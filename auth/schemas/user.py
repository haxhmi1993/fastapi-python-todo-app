from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
