from typing import Annotated
from sqlalchemy import create_engine
from fastapi import Depends
from sqlmodel import SQLModel,Session
from backend.config import settings

# Create database URL from environment
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Annotated type for dependency injection
SessionDep = Annotated[Session, Depends(get_session)]
