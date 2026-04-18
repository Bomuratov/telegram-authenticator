from pydantic import BaseModel, field_validator
from typing import Any, Dict, Optional
from decimal import Decimal


class FinanceFailPayload(BaseModel):
    order_id: int |  None
    title: str | None
    error: str | None
    trace: Optional[str] = None
    data: Optional[str] = None