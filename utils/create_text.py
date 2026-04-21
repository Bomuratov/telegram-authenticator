from typing import Dict, Any
from schemas.notifications import PaidOrderDTO, PayloadModel, AcceptOrderModel
from zoneinfo import ZoneInfo



# "options": {"id": 92, "name": "0,7", "price": 12000, "is_active": True},
# "delivery_price": 5200,
# "comment": "test test",



# def create_order(payload: PayloadModel):
#     order_id = payload.id
#     total_price = int(payload.order_coast)
#     products = payload.products
#     restaurant = payload.restaurant
#     rest_name = restaurant["name"]
#     lat = payload.lat
#     long = payload.long
#     header = f"<b>Заказ</b> #{order_id}A \n\n"
#     order = "<b>🧾  Состав заказа:</b>\n"
#     warehouse = f"<b>Склад: {rest_name}</b>\n\n"
#     linear = "<b>————————————————</b>\n"
#     info = ""
#     comment = f"⚠️ Комментарий к заказу:\n<b>🚨{payload.comment}🚨</b>" if payload.comment else "⚠️ Комментарий к заказу:\n<b></b>"

#     delivery_price = f"Сумму доставки: {payload.delivery_price} UZS"

#     for product in products:
#         options = product_options = product.get("options")
#         if options:
#             name = product["name"]
#             quantity = product["quantity"]
#             price = product["options"]["price"] or product["price"]
#             line = f"<b>—— {name} ({options['name']}) х {quantity} от {price} сум.</b>\n"
#             info += line
#         else:
#             name = product["name"]
#             quantity = product["quantity"]
#             price = product["price"]
#             line = f"<b>—— {name} х {quantity} от {price} сум.</b>\n"
#             info += line

#     full = (
#         header
#         + warehouse
#         + order
#         + linear
#         + info
#         + linear
#         + f"<b>💳 Итого: {total_price} UZS</b>\n"
#         + linear
#         + comment or None
#     )
#     return full


def create_order(payload: PayloadModel):
    order_id = payload.id
    total_price = int(payload.order_coast)
    products = payload.products
    discount_items = payload.discount_items or []

    restaurant = payload.restaurant
    rest_name = restaurant.get("name")

    header = f"<b>Заказ</b> #{order_id}A \n\n\n"
    warehouse = f"<b>Склад: {rest_name}</b>\n\n\n"

    order_block = "<b>🧾 Состав заказа:</b>\n\n"
    discount_block = "\n\n<b>🎁 Акционные товары:</b>\n\n"

    linear = "<b>———————————————</b>"

    info = ""
    discount_info = ""
    comment = f"\n\n⚠️ Комментарий к заказу:\n<b>🚨{payload.comment}🚨</b>" if payload.comment else ""

    # --- обычные товары ---
    for product in products:
        options = product.get("options")

        name = product.get("name")
        quantity = product.get("quantity")
        price = product.get("price")

        if options:
            opt_name = options.get("name")
            opt_price = options.get("price") or price
            line = f"<b>— {name} ({opt_name}) × {quantity} = {opt_price * quantity} сум</b>\n\n"
        else:
            line = f"<b>— {name} × {quantity} по {price} сум</b>\n\n"

        info += line

    # --- акционные товары ---
    for item in discount_items:
        name = item.name
        quantity = item.quantity
        price = item.price
        original = item.originalPrice

        if original and original > price:
            line = (
                f"<b>— {name} × {quantity}</b>"
                f" по <s>{original * quantity} сум</s> → <b>{price * quantity} сум</b>\n\n"
            )
        else:
            line = f"<b>— {name} × {quantity} = {price * quantity} сум</b>\n\n"

        discount_info += line


    # --- тип оплаты ---
    payment_map = {
        "cash": "💵 Наличными",
        "card": "💳 Карта",
        "online": "🌐 Онлайн",
    }

    payment = payment_map.get(payload.payment_type, payload.payment_type)
    payment_block = f"\n\n<b>Способ оплаты: {payment}</b>\n"

    # --- финальная сборка ---
    full = (
        header
        + warehouse
        + order_block

        + info

        + (discount_block + discount_info if discount_info else "")

        + f"\n\n<b>💳 Итого: {total_price} сум</b>\n"

        + payment_block

        + comment
    
    )

    return full


def accept_text(payload: AcceptOrderModel):
    order_id = payload.id
    courier_name = payload.courier.username
    phone_number = payload.courier.phone_number
    header = f"<b>✅ Заказ</b> #{order_id}A принят.\n"
    body = f"🚖 Курьер: <b>{courier_name}</b>\n"
    contact = f"📞 Номер курьера: <b>{phone_number}</b>\n"
    time_tashkent = payload.courier.accepted_at.astimezone(ZoneInfo("Asia/Tashkent"))
    formatted_time = time_tashkent.strftime("%d.%m.%Y, %H:%M")
    text = f'🕒 Время принятия: <b>{formatted_time}</b>\n'
    footer = "🍔 Статус: <b>Готовится</b>"

    return header + body + contact + text + footer


def order_paid(payload: PaidOrderDTO):
    order_id = payload.order_id
    header = f"<b>✅ Заказ</b> #{order_id}A опалчен.\n"
    footer = f"<b>Можно готовить</b>"
    linear = "<b>————————————————</b>\n"
    return header + linear + footer


