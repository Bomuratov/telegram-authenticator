from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.courier.get_paid_keyboard import (
    get_attach_keyboard,
)
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
import pytz
import requests

from config import settings

tashkent_tz = pytz.timezone("Asia/Tashkent")


class ReceiptState(StatesGroup):
    waiting_for_receipt = State()


pay_router = Router()


@pay_router.callback_query(F.data.startswith("paid:"))
async def handle_paid(callback: types.CallbackQuery):
    payout_id = callback.data.split(":")[1]

    await callback.message.edit_reply_markup(
        reply_markup=get_attach_keyboard(payout_id)
    )

    await callback.answer("📎 Теперь прикрепите чек")


@pay_router.callback_query(F.data.startswith("attach:"))
async def handle_attach(callback: types.CallbackQuery, state: FSMContext):
    payout_id = callback.data.split(":")[1]

    await state.set_state(ReceiptState.waiting_for_receipt)

    prompt_msg = await callback.message.answer("📸 Отправьте скриншот чека")

    await state.update_data(
        payout_id=payout_id,
        chat_id=callback.message.chat.id,
        bot_message_id=callback.message.message_id,
        prompt_message_id=prompt_msg.message_id,  # 🔥 ВОТ ЭТО ВАЖНО
        text=callback.message.text or "",
    )

    await callback.answer()


@pay_router.callback_query(F.data.startswith("reject:"))
async def handle_reject_receipt(callback_query: types.CallbackQuery, state: FSMContext):
    payout_id = callback_query.data.split(":")[1]
    url = "https://new.aurora-api.uz/api/v1/finance/courier/payout/confirm"
    data = {
        "payout_id": payout_id,
        "initiator": f"@{callback_query.from_user.username}",
        "confirmed": False
    }
    new_text = callback_query.message.text + f"\n\n❌ Отказано со стороны @{callback_query.from_user.username}"
    if callback_query.message.caption:
        await callback_query.message.edit_caption(
            caption=new_text,
            parse_mode="HTML"
        )
    else:
        await callback_query.message.edit_text(
            text=new_text,
            parse_mode="HTML"
        )

    await callback_query.answer(f"Отказано со стороны @{callback_query.from_user.username}")
    response = requests.post(url=url, data=data, timeout=5)



@pay_router.message(ReceiptState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):
    now = datetime.now(tashkent_tz).strftime("%d.%m.%y %H:%M")
    state_data = await state.get_data()

    chat_id = state_data["chat_id"]
    payout_id = state_data["payout_id"]
    bot_message_id = state_data["bot_message_id"]
    prompt_message_id = state_data.get("prompt_message_id")
    old_text = state_data.get("text", "")

    file_id = None
    is_photo = False

    # 📌 Проверка файла
    if message.photo:
        file_id = message.photo[-1].file_id
        is_photo = True

    elif message.document:
        file_id = message.document.file_id

    else:
        await message.answer("❗ Отправьте фото или файл чека")
        return  # ❗ ОБЯЗАТЕЛЬНО

    # 📥 скачиваем файл из Telegram
    file = await message.bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{settings.bot.token}/{file.file_path}"

    try:
        file_response = requests.get(file_url, timeout=10)
        file_response.raise_for_status()
    except Exception:
        await message.answer("❌ Ошибка загрузки файла. Попробуйте снова")
        return

    # 📄 имя файла
    if is_photo:
        filename = f"receipt_{payout_id}.jpg"
    else:
        filename = message.document.file_name or f"receipt_{payout_id}"

    files = {
        "receipt": (
            filename,
            file_response.content,
            file_response.headers.get("Content-Type")
        )
    }

    url = "https://new.aurora-api.uz/api/v1/finance/courier/payout/confirm"

    payload = {
        "payout_id": payout_id,
        "initiator": str(message.from_user.username),
        "confirmed": True,
    }

    # 📡 запрос в DRF
    try:
        resp = requests.post(url=url, data=payload, files=files, timeout=10)
        response = resp.json()
    except Exception:
        await message.answer("❌ Ошибка связи с сервером")
        return

    # 🧹 удаляем старые сообщения
    try:
        await message.delete()
        await message.bot.delete_message(chat_id, bot_message_id)
    except:
        pass

    if prompt_message_id:
        try:
            await message.bot.delete_message(chat_id, prompt_message_id)
        except:
            pass

    # 📤 отправка результата
    if response.get("success"):
        caption = (
            f"{old_text}\n\n📎 Чек прикреплён\n"
            f"✅ <b>Оплачен успешно</b>\n"
            f"Оплатил: @{message.from_user.username}\n"
            f"Время: {now}"
        )

        if is_photo:
            await message.bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
            )
        else:
            await message.bot.send_document(
                chat_id=chat_id,
                document=file_id,
                caption=caption,
                parse_mode="HTML",
            )

    else:
        error_text = response.get("detail", {}).get("message", "Ошибка")
        url = "https://new.aurora-api.uz/api/v1/finance/courier/payout/confirm"
        data = {
            "payout_id": payout_id,
            "initiator": f"@{message.from_user.username}",
            "confirmed": False
        }
        requests.post(url=url, data=data, timeout=5)
        caption = (
            f"{old_text}\n\n❌ {error_text}\n"
            f"Время: {now}"
        )

        await message.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode="HTML",
        )

    await state.clear()