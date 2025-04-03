from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from backend import models
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status


SECRET_KEY = "secret"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int):
    to_encode = {"sub": username, "id": user_id}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials by user_id or username",
            )
        return {"user_id": user_id, "username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials by JWT",
        )
