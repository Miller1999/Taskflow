from fastapi import FastAPI
from sqlalchemy.orm import Session
from backend import models, database
from sqlalchemy import text
from .routers import users, projects, tasks, auth

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    db: Session = database.SessionLocal()
    try:
        db.execute(
            text("SELECT 1")
        )  # Se usa text() para compatibilidad con SQLAlchemy 2.0
        return {"status": "OK", "message": "DB Connected"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
    finally:
        db.close()
