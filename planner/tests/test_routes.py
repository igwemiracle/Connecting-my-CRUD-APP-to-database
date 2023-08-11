import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

#===================================================================
# Create a fixture that returns an access token when invoked
# scope="module": this will be passed to the fixture as an argument
#   which specifies that this fixture will be created and available
#   once per module (test file).
#===================================================================
@pytest.fixture(scope="module")
async def access_token() ->str:
    return create_access_token("TestUsername")


@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator = "TestUsername",
        title = "FastAPI Book Launch",
        image ="https://myimage.com/image.png",
        description = "We will be discussing the contents of the FastAPI book",
        tags =["python","fastapi","book","launch"],
        location= "Google Meet"
    )
    await new_event.insert_one(new_event)
    yield new_event

@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient,
                           mock_event:Event, access_token:str) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await default_client.get("/event/", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

@pytest.mark.asyncio
async def test_get_event(default_client:httpx.AsyncClient
                         ,mock_event:Event, access_token:str) ->None:
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url, headers=headers)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

@pytest.mark.asyncio
async def test_post_event(default_client:httpx.AsyncClient,
                           access_token:str, mock_event:Event) ->None:
    payload = {
        "creator": "NameOfUsername",
        "title" : "FastAPI Book Launch",
        "image" :"https://myimage.com/image.png",
        "description" : "We will be discussing the contents of the FastAPI book",
        "tags" :["python","fastapi","book","launch"],
        "location":"Google Meet"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {
        "Message": f"{mock_event.creator}'s Event created successfully."
    }
    response = await default_client.post("/event/new", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

# Test that verifies the count of events stored in database
@pytest.mark.asyncio
async def test_get_events_count(default_client:httpx.AsyncClient,
                                 access_token:str) ->None:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await default_client.get("/event/", headers=headers)
    events = response.json()

    assert response.status_code == 200
    assert len(events) == 2

@pytest.mark.asyncio
async def test_update_event(default_client:httpx.AsyncClient,
                             access_token:str, mock_event:Event) ->None:
    test_payload = {
        "creator": "NameOfUsername",
        "title": "Updated FastAPI title",
        "image" :"https://myimage.com/image.png",
        "description" : "We will be discussing the contents of the FastAPI book",
        "tags" :["python","fastapi","book","launch"],
        "location":"Google Meet"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_response = {
        "Message": "Event deleted successfully."
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


