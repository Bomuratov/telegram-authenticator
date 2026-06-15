from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Request
from config.redis_client import save_order_message
from core.order_context import normalize_source, set_order_source
from schemas.notifications import PayloadModel
from utils.create_text import create_order
from bot.commands import bot




router = APIRouter()


@router.post("/new-order")
async def new_order_notification(payload: PayloadModel, request: Request):
    raw_source = request.headers.get("X-Source")
    source = normalize_source(raw_source)
    print("REQUEST DATA: ",request.body)
    print("PAYLOAD: ",payload.json())

    # ✅ сохраняем source
    await set_order_source(payload.id, source)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=f"choose_time:{payload.id}",  # ❗ БЕЗ source
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_order:{payload.id}",
                ),
            ]
        ]
    )

    msg = await bot.send_message(
        chat_id=payload.orders_chat_id,
        text=create_order(payload),
        parse_mode="html",
        reply_markup=keyboard,
    )

    await save_order_message(
        order_id=payload.id,
        chat_id=payload.orders_chat_id,
        message_id=msg.message_id,
        text=create_order(payload)
    )

    return {"message": "ok"}