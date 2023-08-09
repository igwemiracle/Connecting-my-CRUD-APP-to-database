import logging
from models.users import User
from models.events import Event
import motor
import motor.motor_asyncio
import beanie
import logging



def secret_key() -> bytes:
    SECRET_KEY = b"HI5HL3V3L$3CR3T"
    return SECRET_KEY

# Initializes my database
async def initialize():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/")
    db_name = "user"
    await beanie.init_beanie(database=client[db_name], document_models=[Event, User])
    logging.info(f"Connected to database: {db_name}")




