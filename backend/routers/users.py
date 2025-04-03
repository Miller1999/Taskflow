from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.auth.auth import get_current_user

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user.name} deleted"}


@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_db = db.get(models.User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db
