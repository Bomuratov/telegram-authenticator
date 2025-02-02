from pydantic import BaseModel
from typing import Optional


class ClientCreate(BaseModel):
    chat_id: int
    username: str
    first_name: str
    context: Optional[str]


class ClientGet(ClientCreate):
    id: int

class CodeSchema(BaseModel):
    user_id: str
    data: str