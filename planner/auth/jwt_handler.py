# This file will contain the functions required to encode and decode the JWT strings.
import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from database.connection import secret_key


def create_access_token(user: str) -> str:
    payload = {
        "user": user,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, secret_key(), algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, secret_key(), algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No access token supplied")
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Token expired!")
        return data

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token") from e
