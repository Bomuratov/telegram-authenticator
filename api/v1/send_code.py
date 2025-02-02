from fastapi import APIRouter, status
from config import db_redis
from bot.commands import bot
from aiogram.exceptions import TelegramBadRequest
from utils.encode import encoder
from bot.schemas import CodeSchema


router = APIRouter()


# @router.post("/send_verification_code/")
# async def send_verification_code(request:VerificationRequest, session: AsyncSession = Depends(db_helper.session_getter)):
#     existing_client = await session.execute(
#         select(Client).where(Client.phone == request.phone)
#     )
#     client = existing_client.scalar_one_or_none()

#     if client and client.is_registered:
#         await bot.send_message(client.chat_id, f"Ваш код подтверждения: {request.code}")
#         return {"status": "success", "message": "Код подтверждения отправлен"}
#     else:
#         client = Client(
#             phone=request.phone, 
#             code=request.code
#             )
#         session.add(client)
#         await session.commit()
#         bot_link = f"https://t.me/verify_01_bot/start={request.code}"
#         return {"status": "pending", "message": f"Пожалуйста, перейдите по ссылке на бот для завершения регистрации: {bot_link}"}
    


@router.post("/send_code/")
async def send_code(payload: CodeSchema):
    user_id = encoder(int(payload.user_id))
    db_redis.setex(f"verification:{user_id}", 900, payload.data)
    
    try:
        await bot.send_message(chat_id=user_id, text=f"Ваш код верификации {payload.data} не сообщите его никому. Данный код действителен в течении 15 минут", parse_mode="HTML")
        return {
            "status": status.HTTP_200_OK,
            "detail": "Success"
        }
    except TelegramBadRequest as e:
        return {
            "status": status.HTTP_403_FORBIDDEN,
            "detail": f"https://t.me/aurora_auth_bot?start={user_id}"
        }