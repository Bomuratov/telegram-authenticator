from aiogram import F, types

from bot.commands import bot
from aiogram.exceptions import TelegramBadRequest
from fastapi import APIRouter, HTTPException
from starlette import status
from bot.handlers.courier.get_paid_keyboard import get_pay_keyboard
from bot.handlers.courier.pay_callback import ReceiptState
from schemas.courier_payout import CourierPayout
from utils.courier_payout_text import create_courier_payout_text


router = APIRouter()


@router.post("/courier-payout")
async def notify_courier_payout(payload: CourierPayout):

    text = create_courier_payout_text(payload=payload)

    try:
        await bot.send_message(
            chat_id=str(-5179273025),
            text=text,
            parse_mode="HTML",
            reply_markup=get_pay_keyboard(payload.payout_id)
        )
        return {"message": "Уведомление успешно отправлено", "code": 2}
    
    except TelegramBadRequest as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    



