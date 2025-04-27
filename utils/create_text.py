from typing import Dict, Any
from schemas.notifications import PayloadModel
{
    "id": 1,
    "created_at": "2025-03-23T17:49:37.607Z",
    "updated_at": "2025-03-23T17:49:37.607Z",
    "created_by": "User83",
    "products": [
        {"id": 33, "name": "Картофель Фри", "price": 15000, "quantity": 1},
        {"id": 34, "name": "Картофель Деревенски", "price": 15000, "quantity": 2},
    ],
    "total_price": "45000",
    "lat": "40.7128",
    "long": "-74.0060",
    "user_id": 182,
    "restaurant": {
        "id": 1,
        "name": "string",
        "photo": "string",
        "address": "string",
        "phone": "sda"
                    },
    "status": "pending",
}






def create_order(payload: PayloadModel):
    print(payload)
    order_id = payload.id
    total_price = payload.total_price
    products = payload.products
    restaurant = payload.restaurant
    rest_name = restaurant["name"]
    lat = payload.lat  # например, 41.2995
    long = payload.long  # например, 69.2401
    header = f"<b>Заказ</b> #{order_id}A \n\n"
    order = "<b>🧾  Состав заказа:</b>\n"
    warehouse = f"<b>Склад: {rest_name}</b>\n\n"
    created_by = f"<b>Заказал: {payload.created_by}</b>\n\n"
    linear = "<b>————————————————</b>\n"
    info = ""
    for product in products:
        name = product["name"]
        quantity = product["quantity"]
        price = product["price"]
        line = f"<b>— {name} х {quantity} от {price} сум</b>\n"
        info += line
    full = (
        header
        + warehouse
        + created_by
        + order
        + linear
        + info
        + linear
        + f"<b>💳 Итого: {total_price}</b>\n"
    )
    return full



