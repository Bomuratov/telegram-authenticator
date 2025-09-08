import logging
import requests
from fastapi import APIRouter, status, HTTPException, Request
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import PayloadModel, AcceptOrderModel
from bot.commands import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from utils.create_text import create_order, accept_text

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





@router.post("/new-order")
async def new_order_notification(payload: PayloadModel, request: Request):
    source = request.headers.get("X-Source")


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_order:{payload.id}:{source}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_order:{payload.id}:{source}")
            ]
        ]
    )

    try:
        await bot.send_message(chat_id=payload.orders_chat_id, text=create_order(payload), parse_mode="html", reply_markup=keyboard)

        return {
            "message": "Notify has successfully sended",
            "code": 2
        }
    except TelegramBadRequest as e:
        
        logger.error("Ошибка Telegram: %s", e)

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except requests.RequestException as e:
        
        logger.error("Ошибка запроса к REST API ресторана: %s", e)

        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении orders_chat_id")

    
@router.post("/accept-order")
async def accept_order(payload: AcceptOrderModel):
    try:
        await bot.send_message(chat_id=payload.orders_chat_id, 
                               text=accept_text(payload=payload),
                               parse_mode='HTML')
        return {
            "message": "Уведомление успешно отправлено",
            "code" : 2
        }
    except TelegramBadRequest as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except requests.RequestException as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении orders_chat_id")





