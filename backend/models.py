from typing import Annotated, Optional 

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from backend.enums import feedingMethod
from datetime import datetime 


class FeedingDBModel(SQLModel, table=True):
    __tablename__ = "feeds"

    id: int = Field(default=None, primary_key=True)
    method: feedingMethod 
    time: datetime = Field(default_factory = datetime.now)
    amount_oz: Optional[int] = None
    amount_ml: Optional[int] = None
    notes: Optional[str] = None

# feeding: primary key-id, datetime, feedingMethod(enum),notes, amount_oz,amount_ml