from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from bot.order_callback import logger
from datetime import datetime
import pytz

review_router = Router()

tashkent_tz = pytz.timezone("Asia/Tashkent")
now = datetime.now(tashkent_tz).strftime("%d.%m %H:%M")


@review_router.callback_query(F.data.startswith("review:"))
async def handle_review_action(callback: CallbackQuery):
    print("=== CALLBACK ===")
    print("data:", callback.data)
    print("user_id:", callback.from_user.id)
    print("username:", callback.from_user.username)
    print("chat_id:", callback.message.chat.id if callback.message else None)
    print("================")
    _, action, orderId = callback.data.split(":")

    if action == "take":
        text = f"\n\n🛠 Отзыв #{orderId}A взят в работу оператором @{callback.from_user.username} , \n Время принятия : {now}"

    elif action == "close":
        text = f"✅ Отзыв {orderId} закрыт"

    else:
        text = "⚠️ Неизвестное действие"

    # await callback.message.r
    try:
        await callback.message.edit_text(
            callback.message.text + text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=callback.message.reply_markup,
        )

    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
