from fastapi import APIRouter
from config import settings
from bot.commands import dp, bot
from pydantic import BaseModel
from typing import Optional
from aiogram.types import Update

router = APIRouter()



@router.post(f"{settings.bot.path}")
async def bot_webhook(update: Update):

    await dp.feed_update(bot, update)
