import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings

from bot.webhook import bot, router
from bot.choose_time import bot_router as choose_time_router

from api.v1.send_code import router as send_code
from api.v1.send_notifications import router as send_notify
from api.v1.send_support_case import router as send_support_case
from api.v1.messages import router as messages




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = ["*"]



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("установка вебхука")
    await bot.set_webhook(f"{settings.bot.url}{settings.bot.path}")
    yield
    logger.info("Заканчиваем работу")
    await bot.session.close()
    logger.info(f"Сессия бота закрыт: ")


fapp = FastAPI(lifespan=lifespan, root_path="/fastapi")
fapp.include_router(router, tags=["webhook"])
fapp.include_router(send_code, tags=["send_code"])
fapp.include_router(send_notify, tags=["send_notify"])
fapp.include_router(send_support_case, tags=["send_support_case"])
fapp.include_router(choose_time_router, tags=["choose_time_router"])
fapp.include_router(messages, tags=["messages"])



fapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)