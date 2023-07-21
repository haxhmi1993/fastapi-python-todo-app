from fastapi import APIRouter, Depends
from ..schemas.channel import CreateChannel
from ..models import Channels
from sqlalchemy.orm import Session
from ...common.responses import success_response
from config.db.database_config import get_db
from ...common.exceptions import http_exception

router = APIRouter(
    prefix='/channels',
    tags=['/channels'],
    responses={401: {"channel": "not found"}}
)


@router.post("/create-channel")
async def create_channel(create_channel: CreateChannel, db: Session = Depends(get_db)):
    create_channel_model = Channels(**create_channel.model_dump())
    db.add(create_channel_model)
    db.commit()
    return success_response(201)


@router.get("/")
async def get_channels(db: Session = Depends(get_db)):
    return db.query(Channels).all()


@router.get("/{channel_id}")
async def get_channel_by_id(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channels).filter(Channels.id == channel_id).first()
    if channel is None:
        raise http_exception(404, 'Channel not found')
    return channel
