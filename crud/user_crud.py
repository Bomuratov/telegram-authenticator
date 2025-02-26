# from fastapi import status, HTTPException
# from sqlalchemy import select, update
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.engine import Result
# from sqlalchemy import text
# from config import db_helper  # Импортируем наш DatabaseHelper

# class UserCrud:
#     def __init__(self):
#         pass

#     async def update_chat_id(phone: str, new_chat_id: int):
#         async with db_helper.session_getter() as session:
#             sql = text("UPDATE authentication_usermodel SET chat_id = :chat_id WHERE phone = :phone")
#             await session.execute(sql, {"chat_id": new_chat_id, "phone": phone})
#             await session.commit()  # Фиксируем изменения
#             return {"message":f"Chat ID обновлён для {phone}"}

#     async def get_chat_id_by_phone(phone: str, session: AsyncSession):
#         sql = text("SELECT email FROM authentication_usermodel WHERE phone = :phone")
#         result = await session.execute(sql, {"phone": phone})
#         chat_id = result.scalar()  # Получаем значение из первой строки
#         return chat_id