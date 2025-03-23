import requests
from fastapi import BackgroundTasks
from aiogram import Router, types


bot_router = Router()


def send_order_update(order_id: str, status: str):

    """Фоновая задача для отправки PUT-запроса на backend"""

    url = f"https://backend.aurora-app.uz/api/orders/update/{order_id}"
    headers = {'Content-Type': 'application/json'}
    data = {"status": status}

    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"✅ Ответ от сервера ({status}):", response.status_code, response.text)
    except Exception as e:
        print(f"❌ Ошибка при обновлении заказа #{order_id}: {e}")


@bot_router.callback_query(
    lambda c: c.data.startswith("accept_order") or c.data.startswith("reject_order")
)
async def handle_order_action(callback_query: types.CallbackQuery, background_tasks: BackgroundTasks):

    action, order_id = callback_query.data.split(":", 6)

    if action == "accept_order":
        text = f"✅ Заказ #{order_id} принял пользователь @{callback_query.from_user.username}"
        status = "prepare"
    elif action == "reject_order":
        text = f"❌ Заказ #{order_id} отменил пользователь @{callback_query.from_user.username}"
        status = "canceled"
    else:
        await callback_query.answer("Ошибка! Неизвестное действие.")
        return
    
    await callback_query.message.reply(text)
    await callback_query.message.delete_reply_markup()

    background_tasks.add_task(send_order_update, order_id, status)