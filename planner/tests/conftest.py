#This is the umbrella test file which will be responsible
#for creating an instance of our application required by the test files.

import asyncio
import httpx
import pytest

from main import app
from database.connection  import initialize_database, database_url
from models.events import Event
from models.users import User

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

async def init_db():
    test_init = initialize_database()
    await database_url()
    await asyncio.sleep(2)
    await test_init



@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app,
                                 base_url="http://app") as client:
        yield client
        #clean up resources
        await Event.find_all().delete()
        await User.find_all().delete()