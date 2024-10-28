from pydantic import BaseModel
from typing import Optional


class ClientCreate(BaseModel):
    chat_id: int
    username: str
    first_name: str
    context: Optional[str]


class ClientGet(ClientCreate):
    id: int

class VerificationRequest(BaseModel):
    phone: str
    code: str