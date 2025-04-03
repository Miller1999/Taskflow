from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.auth.auth import get_current_user

router = APIRouter(
    prefix="/projects", tags=["Projects"], dependencies=[Depends(get_current_user)]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project {project.name} deleted"}


@router.patch("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    project_db = db.get(models.Project, project_id)
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")

    project_data = project.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(project_db, key, value)

    db.add(project_db)
    db.commit()
    db.refresh(project_db)
    return project_db
