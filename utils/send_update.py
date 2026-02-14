import logging
import requests
import asyncio


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_order_update(order_id: int, status: str):
    """Фоновая задача для отправки PUT-запроса на backend"""
    url = f"https://new.aurora-api.uz/api-node/api/orders/update/{order_id}/"
    headers = {"Content-Type": "application/json"}
    data = {
        "status": status
        # "preparation_time": body
    }

    logger.info("Запуск функции для прод сервера")

    try:
        response = await asyncio.to_thread(
            requests.put, url, json=data, headers=headers
        )
        return response
    except Exception as e:
        logger.error(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")


async def send_stage_order_update(order_id: int, status: str):
    """Фоновая задача для отправки PUT-запроса на backend"""
    url = f"https://stage.aurora-api.uz/api-node/api/orders/update/{order_id}/"
    headers = {"Content-Type": "application/json"}
    data = {
        "status": status
        # "preparation_time": body
    }

    logger.info("Запуск функции для прод сервера")
    logger.info(url)
    try:
        response = await asyncio.to_thread(
            requests.put, url, json=data, headers=headers
        )
    except Exception as e:
        logger.error(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")
