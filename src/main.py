from fastapi import FastAPI
from config.db.database_config import get_db
import logging
from modules.todos.router import router as TodoRouter
from modules.users.router import router as UserRouter
from modules.auth.router import router as AuthRouter
from modules.messaging.routers.group_router import router as MessagingGroupRouter
from modules.messaging.routers.channel_routers import router as MessagingChannelRouter
from modules.messaging.routers.messages_router import router as MessagingMessageRouter


# App Instance
app = FastAPI()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routes Conf
app.include_router(TodoRouter)
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(MessagingGroupRouter)
app.include_router(MessagingChannelRouter)
app.include_router(MessagingMessageRouter)


# DB Conf
@app.on_event('startup')
async def startup_event():
    logger.info('Connecting to Database')

    with next(get_db()) as db:
        logger.info("Database connected successfully")


# Base Route
@app.get('/')
async def root():
    return {'Welcome to FASTAPI'}
