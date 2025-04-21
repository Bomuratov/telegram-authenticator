import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from bot.webhook import bot, router
from api.v1.send_code import router as send_code
from api.v1.send_notifications import router as send_notify





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



fapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)