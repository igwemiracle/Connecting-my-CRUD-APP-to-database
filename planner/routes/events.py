from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from models.events import Event
from typing import List
from auth.authenticate import authenticate

event_router = APIRouter(tags=["Events"])


@event_router.get("/", status_code=200)
async def retrieve_all_events(user: str = Depends(authenticate)) -> List[Event]:
    events = await Event.find({"creator": user}).to_list()
    return events


@event_router.get("/{even_id}", response_model=Event)
async def retrieve_event(even_id: PydanticObjectId, user: str = Depends(authenticate)) -> Event:
    event_to_get = await Event.get(even_id)
    return event_to_get

@event_router.post("/new", status_code=200)
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await body.create()
    return {
        "Message": f"{body.creator}'s Event created successfully."
    }


@event_router.put("/{event_id}", status_code=200)
async def update_event(event: Event, event_id: PydanticObjectId,
                       user:str = Depends(authenticate)) -> Event:
    event_to_update = await Event.get(event_id)
    if not event_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    event_to_update.title = event.title
    event_to_update.image = event.image
    event_to_update.description = event.description
    event_to_update.tags = event.tags
    event_to_update.location = event.location
    await event_to_update.save()
    return event_to_update


@event_router.delete("/{event_id}", status_code=200)
async def delete_event(event_id: PydanticObjectId, user:str = Depends(authenticate)):
    event_to_delete = await Event.get(event_id)
    if not event_to_delete:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    await event_to_delete.delete()
    return {
        "Message": "Event deleted successfully."
    }
