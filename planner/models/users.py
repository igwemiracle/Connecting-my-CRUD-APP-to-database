from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from models.events import Event
from bson import ObjectId
from beanie import PydanticObjectId


class User(Document):
    id: PydanticObjectId = ObjectId
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]]

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": [],
            }}


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
