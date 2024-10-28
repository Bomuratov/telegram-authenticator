from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings, db_helper
from bot.webhook import bot, router
from api.v1.send_code import router as send_code



origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(f"{settings.bot.webhook_url}{settings.bot.webhook_path}{settings.bot.token}")
    print("Вебхук успешно установлен")
    yield
    print("Заканчиваем работу")
    await bot.delete_webhook()
    await bot.session.close()
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["webhook"])
app.include_router(send_code, tags=["send_code"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)