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


class SupportModel(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    subject: str
    message: str
    attachment: Optional[str] = None

# {
#     "created_by": "Gulyamov Mirzogulyam",
#     "products": [
#         {
#             "id": 17,
#             "name": "Греческий",
#             "price": 25000,
#             "photo": "https://new.aurora-api.uz/media/Olivia/category/%D0%A1%D0%B0%D0%BB%D0%B0%D1%82%D1%8B/%D0%93%D1%80%D0%B5%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9.jpg",
#             "options": {
#                 "id": 89,
#                 "name": "1",
#                 "price": 45000,
#                 "is_active": true
#             },
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
#     "total_price": 278500,
#     "lat": "39.74683768921751",
#     "long": "64.41118611988594",
#     "user_id": 2,
#     "user_phone_number": "+998934733223",
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
#         "id": 150,
#         "lat": "39.74683768921751",
#         "long": "64.41118611988594",
#         "address": "улица Абдулазима Сами, 5Б микрорайон",
#         "street": null,
#         "name": "Дом",
#         "house": null,
#         "apartment": "1",
#         "floor": "3",
#         "entrance": "10",
#         "comment": "",
#         "is_active": true,
#         "user": 2
#     },
#     "status": "new",
#     "destination": {
#         "distance": "6.3 km",
#         "duration": "14 mins"
#     },
#     "delivery_price": 0,
#     "comment": "",
#     "courier": null,
#     "fee": 3500,
#     "id": 1578,
#     "created_at": "2025-08-19T04:32:56.226Z",
#     "updated_at": "2025-08-19T04:32:56.226Z"
# }

