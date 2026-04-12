import asyncio
import requests
import logging
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from utils.send_update import send_order_update, send_stage_order_update

uz_time = datetime.now(ZoneInfo("Asia/Tashkent"))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot_router = Router()


@bot_router.callback_query(F.data.startswith("reject_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    # try:
    #     await callback_query.answer("Запрос обработан...")

    # except TelegramBadRequest as e:
    #     logger.error("Ошибка Telegram: %s", e)
    #     return
    try:
        _, order_id, source = callback_query.data.split(":", 2)
        logger.info(f"Извлекаем: base_url='{source}'")
    except ValueError as e:
        logger.error(
            f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}"
        )

    text = (
        f"\n\n❌ Заказ #{order_id} отменил пользователь "
        f"{callback_query.from_user.first_name or ''} "
        f"{callback_query.from_user.last_name or ''}"
    )

    status = "canceled"

    try:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            callback_query.message.text + text,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    if source == "stage":
        logger.info("Запуск функции для стейдж сервера")
        asyncio.create_task(send_stage_order_update(int(order_id), status))
    else:
        logger.info("Запуск функции для прод сервера")
        asyncio.create_task(send_order_update(int(order_id), status))


@bot_router.callback_query(F.data.startswith("accept_order"))
async def action_accept_order(callback_query: types.CallbackQuery):
    # try:
    #     await callback_query.answer("Запрос обработан...")

    # except TelegramBadRequest as e:
    #     logger.error("Ошибка Telegram: %s", e)
    #     return
    try:
        _, order_id, source = callback_query.data.split(":", 2)
        logger.info(f"Извлекаем: base_url='{source}'")
    except ValueError as e:
        logger.error(
            f"Ошибка разбора callback_data: {callback_query.data}, ошибка: {e}"
        )

    text = (
        f"\n\n✅ Заказ #{order_id} принял пользователь "
        f"{callback_query.from_user.first_name or ''} "
        f"{callback_query.from_user.last_name or ''}"
    )

    status = "issued"

    try:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            callback_query.message.text + text,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    except TelegramBadRequest as e:
        logger.error("Ошибка Telegram: %s", e)
        return

    logger.info("Передаем функцию send_order_update вфоновой задачи")
    if source == "stage":
        logger.info("Запуск функции для стейдж сервера")
        asyncio.create_task(send_stage_order_update(int(order_id), status))
    else:
        logger.info("Запуск функции для прод сервера")
        asyncio.create_task(send_order_update(int(order_id), status))


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


@bot_router.callback_query(F.data.startswith("set_time"))
async def set_time(callback_query: types.CallbackQuery):
    # await callback_query.answer()

    _, order_id, source, minutes = callback_query.data.split(":", 3)

    time = uz_time + timedelta(minutes=int(minutes))

    text = (
        f"\n\n✅ Заказ #{order_id} принял пользователь "
        f"{callback_query.from_user.first_name or ''} "
        f"{callback_query.from_user.last_name or ''}"
        f"\n⏱ Время приготовления: <b>{minutes} минут</b>"
    )

    body = {
        "fullTime": time.strftime("%Y.%m.%d %H:%M"),
        "time": time.strftime("%H:%M"),
        "preparationMinutes": int(minutes),
        "acceptedBy": f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}",
        "operatorLogin": f"@{callback_query.from_user.username}",
    }
    print(body)
    status = "awaiting_courier"

    try:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            callback_query.message.text + text, parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        logger.error(e)
        return

    if source == "stage":
        url = f"https://stage.aurora-api.uz/api-node/api/orders/update/{order_id}/"

    else:
        url = f"https://new.aurora-api.uz/api-node/api/orders/update/{order_id}/"
    
    headers = {"Content-Type": "application/json"}
    data = {"status": status, "preparation_time": body}
    resp = requests.put(url, json=data, headers=headers)
    return resp
    # отправляем обновление на сервер
