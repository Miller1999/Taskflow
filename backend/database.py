from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
