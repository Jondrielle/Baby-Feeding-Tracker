from dotenv import load_dotenv
import os
from typing import Annotated
from sqlalchemy import create_engine
from fastapi import Depends
from sqlmodel import SQLModel,Session

# Determine environment
env = os.getenv("ENV", "testing")  # default to production

if env == "testing":
    load_dotenv(".env.testing")
else:
    load_dotenv(".env.production")

# Create database URL from environment
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
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
