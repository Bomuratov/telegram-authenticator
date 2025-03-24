from fastapi import APIRouter, status, HTTPException
import requests
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import NotifyModel
from bot.commands import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, Any
from utils.create_text import create_order

router = APIRouter()


@router.post("/new-order/")
async def new_order_notification(payload: Dict[str, Any]):

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

"""