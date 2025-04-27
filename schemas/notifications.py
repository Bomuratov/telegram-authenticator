from pydantic import BaseModel
from typing import Dict, Any, List


class NotifyModel(BaseModel):
    restaurant_id: int
    body: Dict[str, Any]


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


class CourierModel(BaseModel):
    first_name: str
    last_name: str


class AcceptOrderModel(BaseModel):
    id: int
    orders_chat_id: str
    courier: CourierModel

