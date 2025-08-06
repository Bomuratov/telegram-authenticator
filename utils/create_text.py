from typing import Dict, Any
from schemas.notifications import PayloadModel, AcceptOrderModel



#   "options": {"id": 92, "name": "0,7", "price": 12000, "is_active": True},
# "delivery_price": 5200,
# "comment": "test test",



def create_order(payload: PayloadModel):
    order_id = payload.id
    total_price = payload.total_price
    products = payload.products
    restaurant = payload.restaurant
    rest_name = restaurant["name"]
    lat = payload.lat
    long = payload.long
    header = f"<b>Заказ</b> #{order_id}A \n\n"
    order = "<b>🧾  Состав заказа:</b>\n"
    warehouse = f"<b>Склад: {rest_name}</b>\n\n"
    created_by = f"<b>Заказал: {payload.created_by} {payload.user_phone_number}</b>\n"
    linear = "<b>————————————————</b>\n"
    info = ""
    comment = f"Комментарий к заказу: {payload.comment}"
    delivery_price = f"Сумму доставки: {payload.delivery_price} UZS"
    location = f"Адрес доставки: {payload.location['address'] if payload.location['address'] else ''}\n\n"
    # if options:
    #     for product in products:
    #         name = product["name"]
    #         quantity = product["quantity"]
    #         price = product["price"]
    #         option_name = product["options"]["name"] if "options" in product else "Без опций"
    #         line = f"<b>— {name} ({option_name}) х {quantity} от {price} сум</b>\n"
    #         info += line

    for product in products:
        options = product_options = product.get("options")
        if options:
            name = product["name"]
            quantity = product["quantity"]
            price = product["price"]
            line = f"<b>—— {name} ({options['name']}) х {quantity} от {price} сум.</b>\n"
            info += line
        else:
            name = product["name"]
            quantity = product["quantity"]
            price = product["price"]
            line = f"<b>—— {name} х {quantity} от {price} сум.</b>\n"
            info += line

    full = (
        header
        + warehouse
        + created_by
        + location
        + order
        + linear
        + info
        + linear
        + f"<b>💳 Итого: {total_price} UZS</b>\n"
        + linear
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
    time = f'🕒 Время принятия: <b>{payload.courier.accepted_at.strftime("%d.%m.%Y, %H:%M")}</b>\n'
    footer = "🍔 Статус: <b>Готовится</b>"

    return header + body + contact + time + footer



