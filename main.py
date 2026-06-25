import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from bot.webhook import bot, router
from api.v1.send_code import router as send_code
from api.v1.send_notifications import router as send_notify
from api.v1.send_support_case import router as send_support_case
from api.v1.courier_payout_notify import router as courier_payout
from api.v1.order_notification import router as order_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # settings.bot.url = "https://notify.aurora-api.uz"
    # settings.bot.path = "/webHook"
    webhook_url = f"{settings.bot.url.rstrip('/')}{settings.bot.path}"

    logger.info("Устанавливаем Telegram webhook: %s", webhook_url)

    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=False,
    )

    webhook_info = await bot.get_webhook_info()
    logger.info(
        "Webhook status: url=%s, pending=%s, allowed_updates=%s, last_error=%s",
        webhook_info.url,
        webhook_info.pending_update_count,
        webhook_info.allowed_updates,
        webhook_info.last_error_message,
    )

    yield

    logger.info("Заканчиваем работу")
    await bot.session.close()
    logger.info("Сессия бота закрыта")


fapp = FastAPI(
    lifespan=lifespan,
    root_path="/fastapi",
)

fapp.include_router(router, tags=["webhook"])
fapp.include_router(send_code, tags=["send_code"])
fapp.include_router(send_notify, tags=["send_notify"])
fapp.include_router(send_support_case, tags=["send_support_case"])
fapp.include_router(courier_payout, tags=["courier_payout"])
fapp.include_router(order_router, tags=["order_router"])

fapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)