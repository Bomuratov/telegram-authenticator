from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot_router import bot_router
from aiogram.filters import F
from asyncio.log import logger
from fastapi import APIRouter


bot_router = APIRouter()


@bot_router.callback_query(F.data.startswith("choose_time"))
async def choose_time(callback_query: types.CallbackQuery):
    # await callback_query.answer()

    _, order_id, source = callback_query.data.split(":", 2)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="5 мин", callback_data=f"set_time:{order_id}:{source}:5"
                ),
                InlineKeyboardButton(
                    text="10 мин", callback_data=f"set_time:{order_id}:{source}:10"
                ),
                InlineKeyboardButton(
                    text="15 мин", callback_data=f"set_time:{order_id}:{source}:15"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="20 мин", callback_data=f"set_time:{order_id}:{source}:20"
                ),
                InlineKeyboardButton(
                    text="25 мин", callback_data=f"set_time:{order_id}:{source}:25"
                ),
                InlineKeyboardButton(
                    text="30 мин", callback_data=f"set_time:{order_id}:{source}:30"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="35 мин", callback_data=f"set_time:{order_id}:{source}:35"
                ),
                InlineKeyboardButton(
                    text="40 мин", callback_data=f"set_time:{order_id}:{source}:40"
                ),
                InlineKeyboardButton(
                    text="45 мин", callback_data=f"set_time:{order_id}:{source}:45"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="50 мин", callback_data=f"set_time:{order_id}:{source}:50"
                ),
                InlineKeyboardButton(
                    text="55 мин", callback_data=f"set_time:{order_id}:{source}:55"
                ),
                InlineKeyboardButton(
                    text="60 мин", callback_data=f"set_time:{order_id}:{source}:60"
                ),
            ],
        ]
    )

    try:
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    except TelegramBadRequest as e:
        logger.error(e)