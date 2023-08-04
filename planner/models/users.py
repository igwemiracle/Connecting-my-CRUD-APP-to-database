from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from models.events import Event
from bson import ObjectId
from beanie import PydanticObjectId


class User(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "id": "64cb9225445c574effe9eb1f",
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }}


class UserSignIn(BaseModel):
    id: Optional[PydanticObjectId]
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "id": "64cb9225445c574effe9eb1f",
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }}
