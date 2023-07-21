from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db.database_config import get_db
from ..schemas.group import CreateGroup, JoinGroup
from ..models import Groups
from modules.users.models import Users
from ...common.responses import success_response
from ...common.exceptions import http_exception
from typing import List


router = APIRouter(
    prefix='/groups',
    tags=['/groups'],
    responses={401: {"group": "not found"}}
)


@router.post('/create_group')
async def create_new_group(create_group: CreateGroup, db: Session = Depends(get_db)):
    create_group_model = Groups(**create_group.model_dump())
    db.add(create_group_model)
    db.commit()
    return success_response(201)


@router.get("/")
async def get_groups(db: Session = Depends(get_db)):
    return db.query(Groups).all()


@router.get("/{group_id}")
async def get_group_by_id(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.id == group_id).first()
    if group is None:
        raise http_exception(404, f"Group with id {group_id} not found")
    return group


@router.post("/join-group")
async def join_group(join_group: JoinGroup, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.id == join_group.group_id).first()
    user = db.query(Users).filter(Users.id == join_group.user_id).first()

    if group is None:
        raise http_exception(404, 'No such group exists')
    if user is None:
        raise http_exception(404, 'No such user exists')

    group.joined_users.append(user)
    db.commit()
    return success_response(200)


@router.get("/group_users/{group_name}")
async def get_group_users(group_name: str, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.name == group_name).first()

    if not group:
        raise http_exception(404, 'No such group exists')

    return group.joined_users
