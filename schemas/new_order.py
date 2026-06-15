from typing import Optional, List
from pydantic import BaseModel


class DiscountPercentInfo(BaseModel):
    id: int
    text: str
    type: str
    discount_sum: int
    discount_price: int
    discount_value: int


class ProductItem(BaseModel):
    id: int
    name: str
    photo: str
    price: int
    discount: bool
    quantity: int
    container: bool
    discount_info: Optional[DiscountPercentInfo] = None
    container_info: Optional[dict] = None


class DiscountItem(BaseModel):
    id: int
    name: str
    photo: str
    quantity: int
    price: int
    originalPrice: int


class ContainerItem(BaseModel):
    id: int
    name: str
    size: str
    photo: str
    price: int
    quantity: int
    is_active: bool


class RestaurantInfo(BaseModel):
    id: int
    lat: str
    long: str
    name: str
    phone: str
    photo: str
    address: str


class LocationInfo(BaseModel):
    id: int
    lat: str
    long: str
    name: str
    user: int
    floor: str
    house: Optional[str] = None
    street: Optional[str] = None
    address: str
    city_en: str
    city_ru: str
    comment: str
    entrance: str
    key_zone: str
    state_en: str
    state_ru: str
    apartment: str
    county_en: Optional[str] = None
    county_ru: Optional[str] = None
    is_active: bool
    country_en: str
    country_ru: str
    delivery_zone: str
    is_deliverable: bool


class CourierInfo(BaseModel):
    id: int
    username: str
    phone_number: str


class DestinationInfo(BaseModel):
    distance: str
    duration: str


class PreparationTimeInfo(BaseModel):
    time: str
    fullTime: str
    acceptedBy: str
    operatorLogin: str
    preparationMinutes: int


class PayloadModel(BaseModel):
    id: int
    created_at: str
    updated_at: str
    created_by: str

    products: List[ProductItem]

    total_price: str

    lat: str
    long: str

    user_id: int
    user_phone_number: str
    orders_chat_id: Optional[str] = None

    restaurant: RestaurantInfo
    location: LocationInfo

    status: str

    courier: Optional[CourierInfo] = None
    destination: Optional[DestinationInfo] = None

    fee: int
    delivery_price: int

    comment: str

    preparation_time: Optional[PreparationTimeInfo] = None

    order_coast: str
    payment_type: str
    payment_status: str
    reviewStatus: str

    discount_items: List[DiscountItem] = []
    containers: List[ContainerItem] = []