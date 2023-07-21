from pydantic import BaseModel
from typing import Optional


class CreateChannel(BaseModel):
    name: str
    is_private: Optional[bool] = False
