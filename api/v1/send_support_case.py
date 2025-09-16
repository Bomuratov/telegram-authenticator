import logging
import base64
from fastapi import APIRouter, status, HTTPException
from aiogram.exceptions import TelegramBadRequest
from schemas.notifications import SupportModel
from bot.commands import bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


async def support_case(data: SupportModel):
    caption = (
        f"📩 <b>Новое Обращение</b>\n"
        f"👤 Имя: {data.name}\n"
        f"📧 Email: {data.email or '-'}\n"
        f"📱 Телефон: {data.phone}\n"
        f"📝 Тема: {data.subject}\n"
        f"💬 Сообщение: {data.message}"
    )

    try:
        if data.attachment:
            try:
                photo_bytes = base64.b64decode(data.attachment)
            except Exception:
                raise HTTPException(status_code=400, detail="Неверный формат base64")

            await bot.send_photo(
                chat_id="-1002641409178",
                photo=photo_bytes,
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                chat_id="-1002641409178",
                text=caption,
                parse_mode="HTML"
            )

        return {
            "message": "Уведомление успешно отправлено",
            "code": 2
        }

    except TelegramBadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))