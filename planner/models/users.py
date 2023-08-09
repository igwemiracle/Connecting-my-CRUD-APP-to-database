from beanie import Document
from pydantic import BaseModel

class User(Document):
    username: str
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "igwemiracle",
                "password": "miracle123"
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


