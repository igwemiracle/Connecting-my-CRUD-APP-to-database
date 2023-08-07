# This file will contain the functions that will be used
# to encrypt the password of a user during sign-up and
# compare passwords during sign-in.
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
