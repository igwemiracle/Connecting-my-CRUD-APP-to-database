from models.users import User
from models.events import Event
import motor
import motor.motor_asyncio
import beanie

# Initializes my database


async def initialize():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/")
    await beanie.init_beanie(database=client.db_name, document_models=[Event, User])
