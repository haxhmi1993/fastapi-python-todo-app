from fastapi import APIRouter, Depends
from config.db.database_config import get_db
from ...common.exceptions import http_exception
from ...common.responses import success_response
from sqlalchemy.orm import Session
from ..schemas.message import CreateMessage
from ..models import Messages, Channels, Groups


router = APIRouter(
    prefix='/messages',
    tags=['/messages'],
    responses={401: {"message": "not found"}}
)


@router.post('/create-message')
async def create_message(create_msg: CreateMessage, db: Session = Depends(get_db)):
    message = Messages(**create_msg.model_dump())
    db.add(message)
    db.commit()
    return success_response(201)


@router.get('/')
async def get_all_messages(db: Session = Depends(get_db)):
    return db.query(Messages).all()


@router.get('/channels-messages/{channel_name}')
async def get_channel_messages(channel_name: str, db: Session = Depends(get_db)):
    channel = db.query(Channels).filter(Channels.name == channel_name).first()

    if not channel:
        raise http_exception(status_code=404, detail="Channel not found")

    messages = db.query(Messages).filter(
        Messages.channel_id == channel.id).all()

    return messages


@router.get('/group-messages/{group_name}')
async def get_group_messages(group_name: str, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.name == group_name).first()

    if not group:
        raise http_exception(status_code=404, detail='Group not found')

    messages = db.query(Messages).filter(Messages.group_id == group.id).all()
    return messages
