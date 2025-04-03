from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.auth.auth import get_current_user

router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task.title} deleted"}


@router.patch("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task_db = db.get(models.Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task_db, key, value)

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db
