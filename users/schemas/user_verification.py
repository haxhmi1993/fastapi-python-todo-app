from pydantic import BaseModel


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
