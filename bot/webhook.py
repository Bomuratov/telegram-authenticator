# from fastapi import APIRouter
# from config import settings
# from bot.commands import dp, bot
# from pydantic import BaseModel
# from typing import Optional
# from aiogram.types import Update


# router = APIRouter()


# @router.post(f"{settings.bot.path}")
# async def bot_webhook(update: Update):
#     await dp.feed_update(bot, update)





import logging

from fastapi import APIRouter, HTTPException, status
from aiogram.types import Update

from config import settings
from bot.commands import dp, bot


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(settings.bot.path, status_code=status.HTTP_200_OK)
async def bot_webhook(update: Update) -> dict[str, bool]:
    logger.warning(
        "Telegram update received: update_id=%s, keys=%s",
        update.update_id,
        [key for key, value in update.model_dump().items() if value is not None],
    )

    if update.callback_query:
        logger.warning(
            "Telegram callback received: callback_id=%s, data=%r, from_user=%s",
            update.callback_query.id,
            update.callback_query.data,
            update.callback_query.from_user.id,
        )

    try:
        await dp.feed_update(bot, update)
    except Exception:
        logger.exception(
            "Failed to process Telegram update: update_id=%s",
            update.update_id,
        )
        # Для Telegram лучше вернуть 200, иначе он будет бесконечно ретраить update.
        # Ошибка уже останется в production-логах.

    return {"ok": True}