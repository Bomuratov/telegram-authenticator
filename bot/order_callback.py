import asyncio
import requests
import logging
import time
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_router = Router()

async def send_order_update(order_id: int, status: str):
    """Фоновая задача для отправки PUT-запроса на backend"""
    url = f"https://new.aurora-api.uz/api-node/api/orders/update/{order_id}/"
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


@bot_router.callback_query(F.data.startswith("reject_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer("Запрос обработан...") 
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    try:
        _, order_id = callback_query.data.split(":", 1)
        logger.info(f"Извлекаем: order_id='{order_id}'")
    except ValueError as e:
        logger.error(f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}")
    


    
    text = f"\n\n❌ Заказ #{order_id} отменил пользователь {callback_query.from_user.first_name} {callback_query.from_user.last_name}"
    logger.info(f"Создали текст: {text}")

    status = "canceled"

    logger.info(f"Создали статус: {status}")
    

    
    try:
        logger.info("Удалили inline-клавиатуры: ✅ Принять")
        await callback_query.message.delete_reply_markup()
        logger.info(f"Отправили сообщение: {text}")  
        await callback_query.message.edit_text(
            callback_query.message.text+text,
            parse_mode="HTML",
            disable_web_page_preview=True
            )
       
        
        
    except TelegramBadRequest as e:
        logger.info(f"##################################")
        logger.error("Ошибка Telegram: %s", e)
        logger.info(f"##################################")
        return
    

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    asyncio.create_task(send_order_update(int(order_id), status))    


@bot_router.callback_query(F.data.startswith("accept_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer("Запрос обработан...") 
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    try:
        _, order_id = callback_query.data.split(":", 1)
        logger.info(f"Извлекаем: order_id='{order_id}'")
    except ValueError as e:
        logger.error(f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}")

    
    text = f"\n\n✅ Заказ #{order_id} принял пользователь {callback_query.from_user.first_name} {callback_query.from_user.last_name} статус заказа изменен на «Ожидании курьера»"
    logger.info(f"Создали текст: {text}")

    status = "awaiting_courier"

    logger.info(f"Создали статус: {status}")
    

    
    try:
        logger.info("Удалили inline-клавиатуры: ✅ Принять")
        await callback_query.message.delete_reply_markup()
        logger.info(f"Отправили сообщение: {text}")  
        await callback_query.message.edit_text(
            callback_query.message.text+text,
            parse_mode="HTML",
            disable_web_page_preview=True
            )

       
        
        
    except TelegramBadRequest as e:
        logger.info(f"##################################")
        logger.error("Ошибка Telegram: %s", e)
        logger.info(f"##################################")
        return
    

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    asyncio.create_task(send_order_update(int(order_id), status)) 