import logging
import requests
from fastapi import APIRouter, status, HTTPException
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import PayloadModel
from bot.commands import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.create_text import create_order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

{
    "created_by": "Super Admin",
    "products": [
        {
            "id": 77,
            "name": "Samsung",
            "photo": "https://new.aurora-api.uz/media/Pasta%20House/category/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B5%20%D0%B1%D0%BB%D1%8E%D0%B4%D0%B0/Samsung.jpeg",
            "price": 1000,
            "quantity": 1
        },
        {
            "id": 116,
            "name": "test",
            "photo": "https://new.aurora-api.uz/media/Pasta%20House/category/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B5%20%D0%B1%D0%BB%D1%8E%D0%B4%D0%B0/test.jpeg",
            "price": 20002,
            "quantity": 1
        }
    ],
    "total_price": 21002,
    "lat": "40.7128",
    "long": "-74.0060",
    "user_id": 1,
    "orders_chat_id": -974972939,
    "restaurant": {
        "id": 1,
        "name": "Pasta House",
        "address": "The Tukimachi street",
        "photo": "https://new.aurora-api.uz/media/Pasta%20House/logo/2024-03-04_12.28.47.jpg",
        "phone": 998934567890
    },
    "status": "new",
    "id": 80,
    "created_at": "2025-04-19T18:57:20.195Z",
    "updated_at": "2025-04-19T18:57:20.195Z"
}





@router.post("/new-order/")
async def new_order_notification(payload: PayloadModel):
    logger.info("Получен запрос на новый заказ с payload: %s", payload)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_order:{payload.id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_order:{payload.id}")
            ]
        ]
    )

    try:
        await bot.send_message(chat_id=payload.orders_chat_id, text=create_order(payload), parse_mode="html", reply_markup=keyboard)
        logger.info(f"##################################")
        logger.info("Сообщение отправлено успешно на chat_id: %s", payload.orders_chat_id)
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