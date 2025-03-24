import logging
import asyncio
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

async def keep_alive():
    """Фоновая задача, чтобы Render не останавливал процесс"""
    while True:
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    url1 = settings.bot.url+settings.bot.path+settings.bot.token
    # print(url1)
    await bot.set_webhook(f"{settings.bot.url}{settings.bot.path}{settings.bot.token}")
    logger.info(f"Вебхук успешно установлен {await bot.get_webhook_info()}")
    task = asyncio.create_task(keep_alive())
    yield
    task.cancel()
    logger.info("Заканчиваем работу")
    # logger.info(f"Удаляем вебхук {await bot.get_webhook_info()}")
    # await bot.delete_webhook()
    # logger.info(f"Вебхук удален: {await bot.get_webhook_info()}")
    await bot.session.close()
    logger.info(f"Сессия бота закрыт: ")
    # await db_helper.dispose()


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

@fapp.get("/health")
async def health_check():
    await bot.set_webhook(f"{settings.bot.url}{settings.bot.path}{settings.bot.token}")
    return {"status": "ok"}