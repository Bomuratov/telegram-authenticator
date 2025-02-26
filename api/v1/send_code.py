import random
from fastapi import APIRouter, status, Depends, Request, HTTPException
from config import db_redis
from bot.commands import bot
from aiogram.exceptions import TelegramBadRequest
from utils.encode import encoder
from bot.schemas import CodeSchema
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
import hmac
import hashlib
from datetime import datetime



router = APIRouter()

@router.post("/send_code/")
async def send_code(payload: CodeSchema):

    user_id = encoder(int(payload.user_id))
    user_phone = payload.user_id
    print(user_phone)
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
    

# @router.post("/send/")
# async def send(phone: str):
#     code = random.randint(100000, 999999)
#     phone = encoder(int(phone))
#     db_redis.setex(f"code_for:{phone}", 900, code)

#     try:
#         await bot.send_message(chat_id=phone, text=f"Ваш код верификации {code} не сообщите его никому. Данный код действителен в течении 15 минут", parse_mode="HTML")
#         return {
#             "status": status.HTTP_200_OK,
#             "detail": "Success"
#         }
#     except TelegramBadRequest as e:
#         return {
#             "status": status.HTTP_403_FORBIDDEN,
#             "detail": f"https://t.me/verify_01_bot?start={phone}"
#         }
    
# @router.post("/get_chat_id/")
# async def get(phone:str, session: AsyncSession = Depends(db_helper.session_getter)):
#     return await UserCrud.get_chat_id_by_phone(phone, session)

GROUP_ID="-974972939"

async def verify_signature(request: Request):
    # Проверка подписи GitHub
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()
    
    secret = settings.git.secret.encode()
    expected = hmac.new(secret, body, hashlib.sha256).hexdigest()
    expected = f"sha256={expected}"
    
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=403, detail="Invalid signature")

@router.post("/git")
async def handle_github_webhook(request: Request):
    await verify_signature(request)
    data = await request.json()
    
    if "push" not in request.headers.get("X-GitHub-Event", ""):
        return {"status": "ignored"}
    
    commit = data.get("head_commit", {})
    author = commit.get("author", {}).get("name", "Unknown")
    branch = data.get("ref", "").split("/")[-1]
    timestamp = commit.get("timestamp", "")
    commit_url = commit.get("url", "")
    repo_url = data.get("repository", {}).get("html_url", "")
    messages = commit.get("message", "")
    
    if timestamp:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        formatted_time = dt.strftime("%d.%m.%Y %H:%M:%S")
    else:
        formatted_time = "N/A"
    message = (
        "💥 <b>Новый коммит!</b>\n"
        f"👨‍💻 <b>Автор:</b> {author}\n"
        f"🪵 <b>Ветка:</b> `{branch}`\n"
        f"📆 <b>Дата:</b> {formatted_time}\n"
        f"📝 <b>Комментарий к коммиту:</b> {messages}\n"
        f"🔗 <b>Ссылка на коммит:</b> <a href='{commit_url}'>click</a>\n"
        f"🔗 <b>Ссылка на pепозиторий:</b> <a href='{repo_url}'>click</a>"
    )
    await bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="HTML")
    return {"status": "ok"}