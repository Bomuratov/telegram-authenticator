import asyncio
import requests
import logging
from aiogram import Router, types


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_router = Router()

async def send_order_update(order_id: int, status: str):
    """Фоновая задача для отправки PUT-запроса на backend"""
    url = f"https://backend.aurora-app.uz/api/orders/update/{order_id}/"
    headers = {'Content-Type': 'application/json'}
    data = {"status": status}

    logger.info(f"##################################")
    logger.info(f"Запуск send_order_update для заказа #{order_id} со статусом '{status}'")
    logger.info(f"##################################")
    try:
        response = await asyncio.to_thread(requests.put, url, json=data, headers=headers)
        logger.info(f"##################################")
        logger.info(f"✅ Ответ от сервера для заказа #{order_id} ({status}): {response.status_code} {response.text}")
        logger.info(f"##################################")
    except Exception as e:
        logger.info(f"##################################")
        logger.error(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")
        logger.info(f"##################################")

@bot_router.callback_query(lambda c: c.data.startswith("accept_order") or c.data.startswith("reject_order"))
async def handle_order_action(callback_query: types.CallbackQuery):
    logger.info(f"##################################")
    logger.info(f"Получен callback: {callback_query.data}")
    logger.info(f"##################################")
    try:
        action, order_id = callback_query.data.split(":", 1)
        order_id = order_id.strip()
        logger.info(f"##################################")
        logger.info(f"Распарсенные данные: action='{action}', order_id='{order_id}'")
        logger.info(f"##################################")
    except ValueError as e:
        logger.info(f"##################################")
        logger.error(f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}")
        logger.info(f"##################################")
        await callback_query.answer("Ошибка! Некорректный формат запроса.")
        return

    if action == "accept_order":
        text = f"✅ Заказ #{order_id} принял пользователь @{callback_query.from_user.username}"
        status = "prepare"
    elif action == "reject_order":
        text = f"❌ Заказ #{order_id} отменил пользователь @{callback_query.from_user.username}"
        status = "canceled"
    else:
        logger.info(f"##################################")
        logger.error(f"Неизвестное действие: {action}")
        logger.info(f"##################################")
        await callback_query.answer("Ошибка! Неизвестное действие.")
        return

    logger.info(f"##################################")
    logger.info(f"Отправка сообщения: {text}")
    logger.info(f"##################################")
    await callback_query.message.reply(text)
    
    try:
        logger.info(f"##################################")
        logger.info("Удаление inline-клавиатуры (reply_markup)")
        logger.info(f"##################################")
        await callback_query.message.delete_reply_markup()
    except Exception as e:
        logger.info(f"##################################")
        logger.warning(f"Ошибка при удалении reply_markup: {e}")
        logger.info(f"##################################")
    logger.info(f"##################################")
    logger.info("Запуск фоновой задачи send_order_update")
    logger.info(f"##################################")
    asyncio.create_task(send_order_update(int(order_id), status))
    
    await callback_query.answer("ok")
