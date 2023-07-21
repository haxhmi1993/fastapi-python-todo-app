from pydantic import BaseModel
from typing import Optional


class CreateMessage(BaseModel):
    message: str
    sender_id: int
    receiver_id: int
    channel_id: int
    group_id: Optional[int] = None
