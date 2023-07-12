from fastapi import APIRouter, Depends
from .schemas.user import CreateUser
from config.db.database_config import get_db
from sqlalchemy.orm import Session
from users.models import Users
from common.responses.responses import success_response
from .context.bcrypt import get_password_hash


router = APIRouter(
    prefix='/auth',
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = Users(**create_user.model_dump())
    create_user_model.hashed_password = get_password_hash(
        create_user.hashed_password)
    db.add(create_user_model)
    db.commit()
    return success_response(201)
