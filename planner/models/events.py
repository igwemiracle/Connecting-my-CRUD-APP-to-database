from beanie import Document
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from beanie import PydanticObjectId


class Event(Document):
    id: PydanticObjectId = ObjectId
    title: str = Field(max_length=100)
    image: str
    description: str = Field(max_length=100)
    tags: List[str]
    location: str = Field(max_length=100)

    class Settings:
        name = "events"

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https:// linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }}


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https:// linktomyimage.com/image.png",
                "description": "We will be discussing MongoDB",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }}
