from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from bot.webhook import bot, router
from api.v1.send_code import router as send_code



origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    url1 = settings.bot.url+settings.bot.path+settings.bot.token
    print(url1)
    await bot.set_webhook(f"{settings.bot.url}{settings.bot.path}{settings.bot.token}")
    print("Вебхук успешно установлен")
    yield
    print("Заканчиваем работу")
    await bot.delete_webhook()
    await bot.session.close()
    # await db_helper.dispose()


fapp = FastAPI(lifespan=lifespan, root_path="/fastapi")
fapp.include_router(router, tags=["webhook"])
fapp.include_router(send_code, tags=["send_code"])


fapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)