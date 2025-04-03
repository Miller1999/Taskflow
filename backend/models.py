from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from . import database
from sqlalchemy.orm import relationship


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    projects = relationship("Project", back_populates="owner")


class Project(database.Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(database.Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
