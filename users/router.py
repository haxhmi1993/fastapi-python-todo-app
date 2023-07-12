from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .models import Users
from config.db.database_config import get_db
from common.exceptions.httpexception import http_exception
from .schemas.user_verification import UserVerification
from auth.exceptions.user_exception import get_user_exception
from auth.context.current_user import get_current_user
from auth.context.bcrypt import get_password_hash, verify_password
from common.responses.responses import success_response, invalid_request_response


router = APIRouter(
    prefix='/users',
    tags=["users"],
    responses={401: {"user": "Not found"}}
)


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(Users).all()


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise http_exception(404, f"User with id {user_id} not found")
    return user


@router.put("/change-password")
async def user_password_change(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.password, user_model.hashed_password):
            user_model.hashed_password = get_password_hash(
                user_verification.new_password)
            db.add(user_model)
            db.commit()
            return success_response(200)
    return invalid_request_response()
