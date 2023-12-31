from fastapi import FastAPI
from config.db.database_config import get_db
import logging


# App Instance
app = FastAPI()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
