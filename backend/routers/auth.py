from fastapi import APIRouter
from starlette import status
from backend import schemas, database, models
from backend.auth import auth
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: schemas.CreateUserRequest, db: Session = Depends(get_db)
):
    user = models.User(
        name=create_user_request.name,
        email=create_user_request.email,
        password=auth.bcrypt_context.hash(create_user_request.password),
    )
    db.add(user)
    db.commit()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    print(user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth.create_access_token(user.email, user.id)
    return {"access_token": token, "token_type": "bearer"}
