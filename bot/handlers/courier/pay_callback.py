from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.courier.get_paid_keyboard import get_attach_keyboard, get_edit_keyboard
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
import pytz


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
        prompt_message_id=prompt_msg.message_id,   # 🔥 ВОТ ЭТО ВАЖНО
        text=callback.message.text or ""
    )

    await callback.answer()

@pay_router.callback_query(F.data.startswith("edit_receipt:"))
async def handle_edit_receipt(callback: types.CallbackQuery, state: FSMContext):
    payout_id = callback.data.split(":")[1]

    await state.set_state(ReceiptState.waiting_for_receipt)

    prompt_msg = await callback.message.answer("📸 Отправьте новый чек")

    await state.update_data(
        payout_id=payout_id,
        chat_id=callback.message.chat.id,
        bot_message_id=callback.message.message_id,  # текущее сообщение с чеком
        prompt_message_id=prompt_msg.message_id,
        text=callback.message.caption or callback.message.text or ""
    )

    await callback.answer("Отправьте новый чек")

@pay_router.message(ReceiptState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):
    now = datetime.now(tashkent_tz).strftime("%d.%m.%y %H:%M")
    data = await state.get_data()

    chat_id = data["chat_id"]
    payout_id = data["payout_id"]
    bot_message_id = data["bot_message_id"]
    prompt_message_id = data["prompt_message_id"]
    old_text = data.get("text", "")

    file_id = None
    is_photo = False

    if message.photo:
        file_id = message.photo[-1].file_id
        is_photo = True

    elif message.document:
        file_id = message.document.file_id

    else:
        await message.answer("❗ Отправьте фото или файл чека")
        return

    # удалить сообщения бота
    try:
        await message.delete()
        await message.bot.delete_message(chat_id, bot_message_id)
    except:
        pass

    try:
        await message.bot.delete_message(chat_id, prompt_message_id)
    except:
        pass

    # отправка
    if is_photo:
        await message.bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption=f"{old_text}\n\n📎 Чек прикреплён\n✅ <b>Оплачен успешно</b>\n Оплатил: @{message.from_user.username}\n Время: {now}",
            reply_markup=get_edit_keyboard(payout_id),  # 👈 добавили
            parse_mode="HTML"
        )
    else:
        await message.bot.send_document(
            chat_id=chat_id,
            document=file_id,
            caption=f"{old_text}\n\n📎 Чек прикреплён\n✅ <b>Оплачен успешно</b>\n Оплатил: @{message.from_user.username} \n Время: {now}",
            reply_markup=get_edit_keyboard(payout_id),  # 👈 добавили
            parse_mode="HTML"
        )

    await state.clear()


