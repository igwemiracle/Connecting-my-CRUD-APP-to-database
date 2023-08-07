from fastapi import APIRouter, HTTPException, status, Depends
from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse


user_router = APIRouter(
    tags=["User"],
)
hash_password = HashPassword()


# @user_router.post("/signup")
# async def sign_user_up(user: User) -> dict:
#     user_exist = await User.find_one(User.email == user.email)

#     if user_exist:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with email provided exists already."
#         )
#     hashed_password = hash_password.create_hash(user.password)
#     user.password = hashed_password
#     print("user.password=======>", user.password)
#     await user.save()
#     return {
#         "message": "User created successfully"
#     }


# @user_router.post("/signin", response_model=TokenResponse)
# async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
#     user_exist = await User.find_one(User.email == user.username)
#     if not user_exist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User with email does not exist."
#         )
#     if hash_password.verify_hash(user.password, user_exist.password):
#         access_token = create_access_token(user_exist.email)
#         return {
#             "access_token": access_token,
#             "token_type": "Bearer"
#         }
#     if user_exist.password == user.password:
#         return {
#             "message": "User signed in successfully."
#         }

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid details passed."
#     )

# ---------------------------------------------------------------
# @user_router.post("/signup")
# async def sign_user_up(user: User) -> dict:
#     user_exist = await User.find_one(User.email == user.email)

#     if user_exist:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with email provided exists already."
#         )
#     await user.save()
#     return {
#         "message": "User created successfully"
#     }


# @user_router.post("/signin")
# async def sign_user_in(user: UserSignIn) -> dict:
#     user_exist = await User.find_one(User.email == user.email)
#     if not user_exist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User with email does not exist."
#         )
#     if user_exist.password == user.password:
#         return {
#             "message": "User signed in successfully."
#         }

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid details passed."
#     )
# # ---------------------------------------------------------------
@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.username == user.username)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with username provided exists already."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    print("HashedPassword======-====>", hashed_password)
    await user.save()
    return {
        "message": "User created successfully"
    }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.username == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with username does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.username)
        return{
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
# ---------------------------------------------------------------
