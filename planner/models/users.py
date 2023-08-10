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
                "username": "UserName",
                "password": "PassWord"
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


