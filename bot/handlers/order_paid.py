from aiogram.exceptions import TelegramBadRequest

from config.redis_client import delete_order_message, get_order_message
from bot.commands import bot



async def handle_order_paid(order_id: int):
    data = await get_order_message(order_id)

    if not data:
        return

    chat_id = data["chat_id"]
    message_id = data["message_id"]

    text = f"✅ Заказ {order_id}A оплачен\n🍳 Можно начинать готовить"

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message_id 
        )
        await delete_order_message(order_id)

    except TelegramBadRequest as e:
        print(f"Telegram error: {e}")


async def handle_order_fail(order_id: int):
    data = await get_order_message(order_id)

    if not data:
        return

    chat_id = data["chat_id"]
    message_id = data["message_id"]

    text = (
        f"❌ Оплата по заказу #{order_id} не выполнена\n"
        f"⏳ Ожидаем оплату от клиента"

    )

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message_id 
        )

    except TelegramBadRequest as e:
        print(f"Telegram error: {e}")