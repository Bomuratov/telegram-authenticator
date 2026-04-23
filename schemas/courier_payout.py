from pydantic import BaseModel
from typing import Optional


class CourierPayout(BaseModel):
    courier_id: int
    created_at: Optional[str] | None
    amount: str
    currency: str
    payout_id: str
    balance_before: str
    balance_after: str
    requested_amount: str
    initiator_id: int