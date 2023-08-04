from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from bson import ObjectId
from beanie import PydanticObjectId

user_router = APIRouter(
    tags=["User"]
)


@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    result = await user.insert_one()
    return {"id": str(result.insert_id)}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.get(User.email == user.email)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exist"
                            )
    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
