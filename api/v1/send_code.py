from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_helper
from bot.models import Client
from bot.commands import bot
from bot.schemas import VerificationRequest


router = APIRouter()


@router.post("/send_verification_code/")
async def send_verification_code(request:VerificationRequest, session: AsyncSession = Depends(db_helper.session_getter)):
    existing_client = await session.execute(
        select(Client).where(Client.phone == request.phone)
    )
    client = existing_client.scalar_one_or_none()

    if client and client.is_registered:
        await bot.send_message(client.chat_id, f"Ваш код подтверждения: {request.code}")
        return {"status": "success", "message": "Код подтверждения отправлен"}
    else:
        client = Client(
            phone=request.phone, 
            code=request.code
            )
        session.add(client)
        await session.commit()
        bot_link = f"https://t.me/tezauth_bot/start={request.code}"
        return {"status": "pending", "message": f"Пожалуйста, перейдите по ссылке на бот для завершения регистрации: {bot_link}"}