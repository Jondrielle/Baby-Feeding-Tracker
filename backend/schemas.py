from fastapi import FastAPI
from pydantic import BaseModel,field_validator,Field,model_validator,field_serializer
from backend.enums import feedingMethod
from datetime import datetime,timezone
from typing import Optional, Self
from backend.utils import ml_to_oz, oz_to_ml
import bleach

class FeedEntry(BaseModel): 
    method: feedingMethod 
    time: datetime = Field(default_factory = datetime.now)
    amount_oz: Optional[int] = None
    amount_ml: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=200)

    @model_validator(mode="after")
    def check_and_normalize_amount(self)-> Self:
        oz = self.amount_oz
        ml = self.amount_ml

        # Must not both be provided
        if oz > 0 and ml > 0:
            raise ValueError("Either amount_oz or amount_ml must be set, not both")

        # Must not both be zero or None
        if (oz is None or oz == 0) and (ml is None or ml == 0):
            raise ValueError("Amount_oz and amount_ml can't both be set to 0")

        amount = oz if oz else ml
        if amount is None or amount <= 0:
            raise ValueError("Feeding amount must be positive and provided in oz or ml")

        # Limit checks
        if oz is not None and oz > 32:
            raise ValueError("Amount exceeds daily maximum (32 oz or 950 ml)")
        if ml is not None and ml > 950:
            raise ValueError("Amount exceeds daily maximum (32 oz or 950 ml)")

        # Convert ml to oz if needed
        if ml is not None and ml > 0:
            self.amount_oz = ml_to_oz(ml)
            self.amount_ml = None # Normalize: store only in oz

        return self

    @field_validator("time",mode = 'after')
    @classmethod
    def time_can_not_be_in_future(cls,value):
        # Ensure `time` is not None
        if value is None:
            raise ValueError("Time cannot be None")

        if value > datetime.now(timezone.utc):
            raise ValueError("Time cannot be in the future")
        return value

    @field_validator("notes",mode="before")
    @classmethod
    def sanitize_notes(cls,notes:str)->str:
        # If notes are None, return an empty string
        if notes is None:
            return ""

        clean_notes = bleach.clean(notes, tags=[], attributes={}, strip=True)
        clean_notes = clean_notes.replace("</script>", "")
        return clean_notes

class FeedEntryID(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def id_must_not_be_none(cls, v):
        if v is None:
            raise ValueError("ID can not be null")
        return v
class FeedEntryResponse(BaseModel):
    id: int 
    method: feedingMethod 
    time: datetime = Field(default_factory = datetime.now)
    amount_oz: Optional[int] = None
    amount_ml: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=200)

    @classmethod 
    def from_db(cls, db_feed):
        return cls(
            id = db_feed.id,
            method= db_feed.method,
            time= db_feed.time,
            amount_oz=db_feed.amount_oz,
            amount_ml=oz_to_ml(db_feed.amount_oz) if db_feed.amount_oz else None,
            notes=db_feed.notes
        )

        @field_serializer("time")
        def serialize_date(self, value: datetime) -> str:
            return value.strftime("%m/%d/%Y %H:%M")

