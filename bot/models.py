# from sqlalchemy.orm import DeclarativeBase, mapped_column
# from sqlalchemy import BigInteger, String, Integer, Boolean


# class Basemodel(DeclarativeBase):
#     __abstract__=True
#     id = mapped_column(Integer, primary_key=True) 


# class Client(Basemodel):
#     __tablename__ = "clients"
#     phone = mapped_column(String, unique=True, nullable=True)
#     chat_id = mapped_column(BigInteger, nullable=True, unique=True)
#     username = mapped_column(String, nullable=True)
#     first_name = mapped_column(String, nullable=True)
#     code = mapped_column(String, nullable=True)
#     is_registered = mapped_column(Boolean, default=False)