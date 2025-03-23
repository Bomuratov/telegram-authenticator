from fastapi import APIRouter, status, HTTPException
import requests
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import NotifyModel
from bot.commands import bot
from utils.create_text import create_order
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, Any

router = APIRouter()

@router.post("/new-order/")
async def new_order_notification(payload: Dict[str, Any]):
    if not payload["restaurant"] :
        raise HTTPException(detail="Не передан chat_id", status_code=status.HTTP_400_BAD_REQUEST)
    restaurant_id = payload["restaurant"]

    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_order: {payload['id']}"),
                    InlineKeyboardButton(text="❌ Отказать", callback_data=f"reject_order: {payload['id']}")
                ]
            ]
        )

    try:
        rest_id = requests.get(url=f"https://stage.aurora-api.uz/api/v1/restaurant/{restaurant_id}/").json()["orders_chat_id"]
        await bot.send_message(chat_id=rest_id, text=create_order(payload), parse_mode="html", reply_markup=keyboard)
        return {
            "message": "Notify has successfully sended",
            "code": 2
                }
    except TelegramBadRequest as e:
        return {"detail": e}
    
