from sqlalchemy import select
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from .models import Client
from config import db_helper, settings

bot = Bot(token=f"{settings.bot.token}")
dp = Dispatcher()



@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Пожалуйста, отправьте свой номер телефона для регистрации", reply_markup=keyboard)


@dp.message(lambda message: message.contact is not None)
async def register_user(message: types.Message):
    if message.contact:
        phone = message.contact.phone_number
        user_id = message.chat.id

        async with db_helper.session_factory() as session:
            result = await session.execute(select(Client).filter(Client.phone == phone))
            user = result.scalars().first()
            if not user:
                user = Client(phone=phone, chat_id=user_id, username=message.chat.username,
                              first_name=message.chat.first_name, is_registered=True)
                session.add(user)
            else:
                user.chat_id = user_id
                user.username = message.chat.username
                user.first_name = message.chat.first_name
                user.is_registered = True
            await session.commit()
        await message.answer(f"Вы успешно зарегистрированы! Ваш проверочный код {user.code}")
    else:
        await message.answer("Ошибка: номер телефона не был отправлен.")