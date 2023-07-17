from fastapi import APIRouter, Depends
from .schemas.user import AuthUser
from config.db.database_config import get_db
from sqlalchemy.orm import Session
from modules.users.models import Users
from modules.common.responses import success_response
from .utils import get_password_hash, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .exceptions import token_exception


router = APIRouter(
    prefix='/auth',
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/create/user")
async def create_new_user(create_user: AuthUser, db: Session = Depends(get_db)):
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
