from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
