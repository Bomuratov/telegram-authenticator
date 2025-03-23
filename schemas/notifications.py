from pydantic import BaseModel
from typing import Dict, Any


class NotifyModel(BaseModel):
    restaurant_id: int
    body: Dict[str, Any]


