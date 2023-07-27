from fastapi import APIRouter, Depends
from sqlalchemy import or_
from config.db.database_config import get_db
from config.main_config import settings
from ...common.exceptions import http_exception
from ...common.responses import success_response
from sqlalchemy.orm import Session
from ..schemas.message import CreateMessage
from ..schemas.paginate import Paginate
from ..models import Messages, Channels, Groups
from pusher import Pusher
from typing import Optional


router = APIRouter(
    prefix='/messages',
    tags=['/messages'],
    responses={401: {"message": "not found"}}
)

# Pusher Configuration for Live Events
pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
)


@router.post('/create-message')
async def create_message(create_msg: CreateMessage, db: Session = Depends(get_db)):
    message = Messages(**create_msg.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    channel = db.query(Channels).filter(
        Channels.id == create_msg.channel_id).first()
    if channel:
        message_response = {
            'id': message.id,
            'message': message.message,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'channel_id': message.channel_id,
            'group_id': message.group_id
        }
        pusher.trigger(channel.name, 'new-message',
                       message_response)
    return success_response(201)


@router.get('/')
async def get_all_messages(db: Session = Depends(get_db)):
    return db.query(Messages).all()


@router.get('/channels-messages/{channel_name}')
async def get_channel_messages(channel_name: str, paginate: Optional[Paginate] = None, db: Session = Depends(get_db)):
    name_parts = channel_name.split('_')
    if len(name_parts) != 2:
        raise http_exception(400, 'Invalid channel name format')
    combined_name_1 = name_parts[0] + '_' + name_parts[1]
    combined_name_2 = name_parts[1] + '_' + name_parts[0]
    channel = db.query(Channels).filter(
        or_(Channels.name == combined_name_1, Channels.name == combined_name_2)).first()
    if channel:
        if paginate is not None:
            messages = db.query(Messages).filter(Messages.channel_id == channel.id).limit(
                paginate.limit).offset(paginate.offset).all()
            return messages
        else:
            messages = db.query(Messages).filter(
                Messages.channel_id == channel.id).all()
            return messages
    else:
        raise http_exception(404, 'channel not found')


@router.get('/group-messages/{group_name}')
async def get_group_messages(group_name: str, db: Session = Depends(get_db)):
    group = db.query(Groups).filter(Groups.name == group_name).first()

    if not group:
        raise http_exception(status_code=404, detail='Group not found')

    messages = db.query(Messages).filter(Messages.group_id == group.id).all()
    return messages
