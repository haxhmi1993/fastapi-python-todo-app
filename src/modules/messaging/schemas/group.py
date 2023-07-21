from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str


class JoinGroup(BaseModel):
    user_id: int
    group_id: int
