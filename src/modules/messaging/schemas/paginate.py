from pydantic import BaseModel
from typing import Optional


class Paginate(BaseModel):
    limit: int
    offset: int
