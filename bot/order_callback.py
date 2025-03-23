import requests
from aiogram import Router, types


bot_router = Router()


@bot_router.callback_query(
    lambda c: c.data.startswith("accept_order") or c.data.startswith("reject_order")
)
async def handle_order_action(callback_query: types.CallbackQuery):

    action, order_id = callback_query.data.split(":", 6)
    headers = {
        'Content-Type': 'application/json',
    }

    if action == "accept_order":
        data = {
        "status": "prepare"
        }
        await callback_query.message.reply(f"✅ Заказ #{order_id} принял пользователь @{callback_query.from_user.username}")
        await callback_query.message.delete_reply_markup()
        response = requests.put(url=f"https://backend.aurora-app.uz/api/orders/update/{order_id}", json=data, headers=headers)
    elif action == "reject_order":
        data = {
        "status": "canceled"
        }
        await callback_query.message.reply(f"❌ Заказ #{order_id} отменил пользователь @{callback_query.from_user.username}")
        await callback_query.message.delete_reply_markup()
        response= requests.put(url=f"https://backend.aurora-app.uz/api/orders/update/{order_id}", json=data, headers=headers)