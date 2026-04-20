from aiogram.exceptions import TelegramBadRequest
from bot.commands import bot

from config.redis_client import delete_order_message, get_order_message


async def handle_order_canceled(order_id: int):
    data = await get_order_message(order_id)

    if not data:
        return {"message": "Order already accepted"}

    chat_id = data["chat_id"]
    message_id = data["message_id"]
    original_text = data["text"]

    new_text = original_text + "\n\n❌ Заказ отменен Пользователем."

    try:
        # убираем кнопки
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )

        # обновляем текст
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
            parse_mode="HTML"
        )

    except TelegramBadRequest as e:
        print(f"Telegram error: {e}")

    # можно удалить из Redis
    await delete_order_message(order_id)
    return {"message": "Order successfully cancelled"}