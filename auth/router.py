from fastapi import APIRouter, Depends
from .schemas.user import CreateUser
from config.db.database_config import get_db
from sqlalchemy.orm import Session
from users.models import Users
from common.responses.responses import success_response
from .context.bcrypt import get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from .context.authenticate import authenticate_user
from datetime import timedelta
from .exceptions.token_exception import token_exception
from .context.token_generate import create_access_token


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


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(
        user.username, user.id, expires_delta=token_expires)
    return {
        "token": token
    }
