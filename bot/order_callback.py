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
    
    logger.info("Запуск функции для прод сервера")
    logger.info(url)

    try:
        response = await asyncio.to_thread(requests.put, url, json=data, headers=headers)
    except Exception as e:
        logger.error(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")


async def send_stage_order_update(order_id: int, status: str):
    """Фоновая задача для отправки PUT-запроса на backend"""
    url = f"https://stage.aurora-api.uz/api-node/api/orders/update/{order_id}/"
    headers = {'Content-Type': 'application/json'}
    data = {"status": status}

    logger.info("Запуск функции для прод сервера")
    logger.info(url)
    try:
        response = await asyncio.to_thread(requests.put, url, json=data, headers=headers)
    except Exception as e:
        logger.error(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")


@bot_router.callback_query(F.data.startswith("reject_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer("Запрос обработан...") 
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    try:
        _, order_id, base_url = callback_query.data.split(":", 2)
        logger.info(f"Извлекаем: base_url='{base_url}'")
    except ValueError as e:
        logger.error(f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}")
    


    
    text = (
    f"\n\n❌ Заказ #{order_id} отменил пользователь "
    f"{callback_query.from_user.first_name or ''} "
    f"{callback_query.from_user.last_name or ''}"
    )

    status = "canceled"

    

    
    try:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            callback_query.message.text+text,
            parse_mode="HTML",
            disable_web_page_preview=True
            )
       
        
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    # if base_url == "stage":
    #     logger.info("Запуск функции для стейдж сервера")
    #     asyncio.create_task(send_stage_order_update(int(order_id), status))
    # if base_url == "prod":
    logger.info("Запуск функции для прод сервера")
    asyncio.create_task(send_order_update(int(order_id), status))    


@bot_router.callback_query(F.data.startswith("accept_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer("Запрос обработан...") 
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    try:
        _, order_id, base_url = callback_query.data.split(":", 2)
        logger.info(f"Извлекаем: base_url='{base_url}'")
    except ValueError as e:
        logger.error(f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}")

    

    text = (
    f"\n\n✅ Заказ #{order_id} принял пользователь "
    f"{callback_query.from_user.first_name or ''} "
    f"{callback_query.from_user.last_name or ''}"
    )

    status = "awaiting_courier"

    

    
    try:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            callback_query.message.text+text,
            parse_mode="HTML",
            disable_web_page_preview=True
            )

       
        
        
    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return
    

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    # if base_url == "http://localhost:8000/fastapi/":
    #     logger.info("Запуск функции для стейдж сервера")
    #     asyncio.create_task(send_stage_order_update(int(order_id), status)) 
    # if base_url == "https://new.aurora-api.uz/api-node":
    logger.info("Запуск функции для прод сервера")
    asyncio.create_task(send_order_update(int(order_id), status)) 





