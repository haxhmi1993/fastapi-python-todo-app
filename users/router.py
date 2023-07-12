from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .models import Users
from config.db.database_config import get_db
from common.exceptions.httpexception import http_exception


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
