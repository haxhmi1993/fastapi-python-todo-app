from fastapi import APIRouter, Depends
from sqlalchemy import or_
from ..schemas.channel import CreateChannel
from ..models import Channels
from sqlalchemy.orm import Session
from ...common.responses import success_response
from config.db.database_config import get_db
from config.main_config import settings
from ...common.exceptions import http_exception
from pusher import Pusher

router = APIRouter(
    prefix='/channels',
    tags=['/channels'],
    responses={401: {"channel": "not found"}}
)

# Pusher Configuration for Live Events
pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
)


@router.post("/create-channel")
async def create_channel(create_channel: CreateChannel, db: Session = Depends(get_db)):
    name_parts = create_channel.name.split('_')
    if len(name_parts) != 2:
        raise http_exception(400, 'Invalid channel name format')
    combined_name_1 = name_parts[0] + '_' + name_parts[1]
    combined_name_2 = name_parts[1] + '_' + name_parts[0]
    channel = db.query(Channels).filter(
        or_(Channels.name == combined_name_1, Channels.name == combined_name_2)).first()
    if channel:
        return channel
    else:
        create_channel_model = Channels(**create_channel.model_dump())
        db.add(create_channel_model)
        db.commit()
        db.refresh(create_channel_model)
        pusher.trigger('channel-create', 'new-channel',
                       {'channel_name': create_channel.name})
        return create_channel_model


@router.get("/")
async def get_channels(db: Session = Depends(get_db)):
    return db.query(Channels).all()


@router.get("/{channel_id}")
async def get_channel_by_id(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channels).filter(Channels.id == channel_id).first()
    if channel is None:
        raise http_exception(404, 'Channel not found')
    return channel


@router.get("/channel-username/{username}")
async def get_channel_by_name(username: str, db: Session = Depends(get_db)):
    channels = db.query(Channels).filter(
        or_(Channels.name.like(f"%{username}%"))).all()
    if not channels:
        raise http_exception(
            404, f'No channels found with username: {username}')
    return channels
