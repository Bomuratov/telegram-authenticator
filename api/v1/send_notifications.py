import logging
from fastapi import APIRouter, status, HTTPException
import requests
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import NotifyModel
from bot.commands import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, Any
from utils.create_text import create_order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/new-order/")
async def new_order_notification(payload: Dict[str, Any]):
    logger.info("Получен запрос на новый заказ с payload: %s", payload)
    try:
        restaurant = payload["restaurant"]
        rest_id = restaurant["id"]
        order_id = payload["id"]

        logger.info(f"##################################")
        logger.info("Извлечены restaurant_id: %s, order_id: %s", restaurant, order_id)
        logger.info(f"##################################")

    except KeyError as e:
        
        logger.info(f"##################################")
        logger.error("Ошибка извлечения ключей из payload: %s", e)
        logger.info(f"##################################")

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отсутствует необходимый параметр")


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_order:{order_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_order:{order_id}")
            ]
        ]
    )
    # logger.info(f"##################################")
    # logger.info("Сформирована inline-клавиатура: %s", keyboard)
    # logger.info(f"##################################")

    try:
        rest_url = f"https://new.aurora-api.uz/api/v1/restaurant/{rest_id}/"

        logger.info(f"##################################")
        logger.info("Запрос к REST API ресторана по URL: %s", rest_url)
        logger.info(f"##################################")

        rest_response = requests.get(url=rest_url)
        rest_response.raise_for_status()
        rest_data = rest_response.json()
        rest_chat_id = rest_data["orders_chat_id"]
        logger.info(f"##################################")
        logger.info("Получен restaurant_response: %s", rest_data)
        logger.info(f"##################################")


        logger.info(f"##################################")
        logger.info("Получен orders_chat_id: %s", rest_chat_id)
        logger.info(f"##################################")

        order_text = create_order(messages=payload)
        # logger.info(f"##################################")
        # logger.info("Сформирован текст заказа: %s", order_text)
        # logger.info(f"##################################")

        await bot.send_message(chat_id=rest_chat_id, text=order_text, parse_mode="html", reply_markup=keyboard)
        logger.info(f"##################################")
        logger.info("Сообщение отправлено успешно на chat_id: %s", rest_chat_id)
        logger.info(f"##################################")

        return {
            "message": "Notify has successfully sended",
            "code": 2
        }
    except TelegramBadRequest as e:
        
        logger.info(f"##################################")
        logger.error("Ошибка Telegram: %s", e)
        logger.info(f"##################################")

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except requests.RequestException as e:
        
        logger.info(f"##################################")
        logger.error("Ошибка запроса к REST API ресторана: %s", e)
        logger.info(f"##################################")

        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении orders_chat_id")

    


""""

import { AccessTime, Close, DoneOutlined, Kitchen, Fastfood } from "@mui/icons-material";
import { Chip } from "@mui/material";

export const getStatusChip = (status: string) => {
  switch (status) {
    case "new":
      return <Chip label="Новый" color="success" icon={<Fastfood />} />;
    case "completed":
      return <Chip label="Готово" color="success" icon={<DoneOutlined />} />;
    case "pending":
      return <Chip label="Ожидание" color="secondary" icon={<AccessTime />} />;
    case "canceled":
      return <Chip label="Отменено" color="error" icon={<Close />} />;
    case "prepare":
      return <Chip label="Готовиться" color="warning" icon={<Kitchen />} />;
    default:
      return <Chip label="Неизвестно" />;
  }
};

curl -X GET "https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo"


"""