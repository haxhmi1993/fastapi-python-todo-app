from fastapi import FastAPI
from config.db.database_config import get_db
import logging
from todos.router import router as TodoRouter


# App Instance
app = FastAPI()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routes Conf
app.include_router(TodoRouter)


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
