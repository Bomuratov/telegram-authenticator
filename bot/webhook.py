from fastapi import APIRouter
from aiogram import types
from config import settings
from bot.commands import dp, bot
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class UpdateSchema(BaseModel):
    update_id: Optional[int]
    message: Optional[dict]


@router.post(f"{settings.bot.path}{settings.bot.token}")
async def bot_webhook(update: UpdateSchema):
    update = types.Update(**update.dict())
    await dp.feed_update(bot, update)
