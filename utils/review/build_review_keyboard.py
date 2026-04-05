from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.notifications import ReviewSchema


def build_review_keyboard(payload: ReviewSchema) -> InlineKeyboardMarkup:
    base_url = "https://dashboard.aurora-app.uz/"

    buttons = []

    # 🔗 Заказ
    if payload.orderId:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="📦 Открыть заказ", url=f"{base_url}dashboard/orders"
                )
            ]
        )

    # 👤 Пользователь
    if payload.userId:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="👤 Пользователь", url=f"{base_url}/users/{payload.userId}"
                )
            ]
        )

    # 🚨 Действия (callback)
    # buttons.append([
    #     InlineKeyboardButton(
    #         text="🚨 В работу",
    #         callback_data=f"review:take:{payload.orderId}"
    #     ),
    #     InlineKeyboardButton(
    #         text="✅ Закрыть",
    #         callback_data=f"review:close:{payload.orderId}"
    #     )
    # ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
