from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from config import settings, db_redis

bot = Bot(token=f"{settings.bot.token}")
dp = Dispatcher()



# @dp.message(Command("startok"))
# async def start(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
#             ],
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#     await message.answer("Пожалуйста, отправьте свой номер телефона для регистрации", reply_markup=keyboard)


# @dp.message(lambda message: message.contact is not None)
# async def register_user(message: types.Message):
#     if message.contact:
#         phone = message.contact.phone_number
#         user_id = message.chat.id

#         async with db_helper.session_factory() as session:
#             result = await session.execute(select(Client).filter(Client.phone == phone))
#             user = result.scalars().first()
#             if not user:
#                 user = Client(phone=phone, chat_id=user_id, username=message.chat.username,
#                               first_name=message.chat.first_name, is_registered=True)
#                 session.add(user)
#             else:
#                 user.chat_id = user_id
#                 user.username = message.chat.username
#                 user.first_name = message.chat.first_name
#                 user.is_registered = True
#             await session.commit()
#         await message.answer(f"Вы успешно зарегистрированы! Ваш проверочный код {user.code}")
#     else:
#         await message.answer("Ошибка: номер телефона не был отправлен.")


# @dp.message(Command("start"))
# async def send_message(message: types.Message):
#     return await bot.send_message(chat_id=message.chat.id, text=f"Твой айди {message.chat.id}")

@dp.message(Command("start"))
async def send_message(message: types.Message):
    phone_id = message.text[7:]
    print(phone_id)
    if not phone_id:
        print(message)
        return await bot.send_message(chat_id=message.chat.id,
                                      text="По вашему номеру телефона не найден проверочный код. Для решения проблемы пройдите регистрацию на сайте aurora-app.uz",
                                      parse_mode="HTML")
    code = db_redis.get(f"verification:{phone_id}")
    if not code:
        return await bot.send_message(chat_id=message.chat.id,
                                      text="Вашему номеру пока не назначен проверочный код или он уже просрочен. Для решения проблемы запросите код заново",
                                      parse_mode="HTML")
    code = code.decode('utf-8') if isinstance(code, bytes) else code
    return await bot.send_message(chat_id=message.chat.id, 
                                  text=f"Ваш код верификации <code><b>{code}</b></code> не сообщите его никому. \nДанный код действителен в течении 15 минут", 
                                  parse_mode="HTML")
