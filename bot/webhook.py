from fastapi import APIRouter
from aiogram import types
from config import settings
from bot.commands import dp, bot


router = APIRouter()


@router.post(f"{settings.bot.path}{settings.bot.token}")
async def bot_webhook(update: dict):
    update = types.Update(**update)
    await dp.feed_update(bot, update)
