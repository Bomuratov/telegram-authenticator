from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class NotifyModel(BaseModel):
    restaurant_id: int
    body: Dict[str, Any]

# class Location(BaseModel):
#     id: int
#     lat: str
#     long: str
#     address: Optional[str]
#     street: Optional[str]
#     name: Optional[str]
#     house: Optional[str]
#     apartment: Optional[str]
#     floor: Optional[str]
#     entrance: Optional[str]
#     comment: Optional[str]
#     comment: bool
#     user: int


class PayloadModel(BaseModel):
    id: int
    created_by: str
    user_id: int
    orders_chat_id: int
    status: str
    lat: str
    long: str
    total_price: int
    updated_at: str
    restaurant: dict
    products: List[dict]
    created_at: str
    comment: str
    delivery_price: int
    user_phone_number: str
    location: dict



class CourierModel(BaseModel):
    id: int
    username: str
    phone_number: str
    accepted_at: datetime


class AcceptOrderModel(BaseModel):
    id: int
    orders_chat_id: str
    courier: CourierModel


# {
#     "created_by": "Мўмин XXX",
#     "products": [
#         {
#             "id": 18,
#             "photo": "https://new.aurora-api.uz/media/Olivia/category/%D0%A1%D0%B0%D0%BB%D0%B0%D1%82%D1%8B/%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8C.jpg",
#             "name": "Цезарь",
#             "price": 35000,
#             "quantity": 1
#         },
#         {
#             "id": 297,
#             "photo": "https://new.aurora-api.uz/media/Olivia/category/%D0%A1%D0%B0%D0%BB%D0%B0%D1%82%D1%8B/%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9_%D1%81%D0%B0%D0%BB%D0%B0%D1%82.jpeg",
#             "name": "новый салат",
#             "price": 230000,
#             "quantity": 1
#         }
#     ],
#     "total_price": 268500,
#     "lat": "39.756475783906225",
#     "long": "64.41936492919922",
#     "user_id": 126,
#     "user_phone_number": "+998931430777",
#     "orders_chat_id": -1002641409178,
#     "restaurant": {
#         "id": 3,
#         "name": "Olivia",
#         "address": "USA California",
#         "photo": "https://new.aurora-api.uz/media/Olivia/logo/0889x24izl.webp",
#         "phone": "+998881836222",
#         "lat": "39.769916",
#         "long": "64.4454786"
#     },
#     "location": {
#         "id": 144,
#         "lat": "39.756475783906225",
#         "long": "64.41936492919922",
#         "address": "Каюма Муртазаева улица, Million, 4 микрорайон, Утрар",
#         "street": null,
#         "name": "",
#         "house": null,
#         "apartment": "",
#         "floor": "",
#         "entrance": "",
#         "comment": "",
#         "is_active": true,
#         "user": 126
#     },
#     "status": "new",
#     "destination": {
#         "distance": "3.4 km",
#         "duration": "9 mins"
#     },
#     "delivery_price": 0,
#     "comment": "",
#     "courier": null,
#     "fee": 3500,
#     "id": 1543,
#     "created_at": "2025-08-06T10:38:01.568Z",
#     "updated_at": "2025-08-06T10:38:01.568Z"
# }