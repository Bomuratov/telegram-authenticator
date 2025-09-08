from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from config import settings
from .order_callback import bot_router


bot = Bot(token=f"{settings.bot.token}")
dp = Dispatcher()
dp.include_router(bot_router)



@dp.message(Command("myid"))
async def send_message(message: types.Message):
    return await bot.send_message(
        chat_id=message.chat.id, text=f"Твой айди {message.chat.id}"
    )

@dp.message(Command("check"))
async def send_message(message: types.Message):
    return await bot.send_message(
        chat_id=message.chat.id, text=f"status : ok\ncode : 200"
    )


@dp.message(Command("start"))
async def send_message(message: types.Message):
    phone_id = message.text[7:]
    print(phone_id)
    if not phone_id:

        return await bot.send_message(
            chat_id=message.chat.id,
            text="По вашему номеру телефона не найден проверочный код. Для решения проблемы пройдите регистрацию на сайте aurora-app.uz",
            parse_mode="HTML",
        )
    code = db_redis.get(f"verification:{phone_id}")
    if not code:
        return await bot.send_message(
            chat_id=message.chat.id,
            text="Вашему номеру пока не назначен проверочный код или он уже просрочен. Для решения проблемы запросите код заново",
            parse_mode="HTML",
        )
    code = code.decode("utf-8") if isinstance(code, bytes) else code
    return await bot.send_message(
        chat_id=message.chat.id,
        text=f"Ваш код верификации <code><b>{code}</b></code> не сообщите его никому. \nДанный код действителен в течении 15 минут",
        parse_mode="HTML",
    )
