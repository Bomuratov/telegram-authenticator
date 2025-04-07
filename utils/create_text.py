from typing import Dict, Any
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
    "restaurant": 3,
    "status": "pending",
}






def create_order(messages: Dict[str, Any], name: str):
    order_id = messages["id"]
    total_price = messages["total_price"]
    products = messages["products"]
    header = f"<b>Заказ</b> #{order_id}A \n\n"
    order = "<b>🧾  Состав заказа:</b>\n"
    warehouse = f"<b>Склад: {name}</b>\n\n"
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
        + order
        + linear
        + info
        + linear
        + f"<b>💳 Итого: {total_price}</b>\n"
    )
    return full


