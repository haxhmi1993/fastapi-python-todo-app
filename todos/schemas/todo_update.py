from pydantic import BaseModel, Field
from typing import Optional


class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(
        gt=0, lt=6, description="The priority must be between 1-5")
    complete: Optional[bool] = None
