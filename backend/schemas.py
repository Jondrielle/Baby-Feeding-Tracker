from fastapi import FastAPI
from pydantic import BaseModel,field_validator,Field,model_validator
from backend.enums import feedingMethod
from datetime import datetime
from typing import Optional
import bleach

class FeedEntry(BaseModel):
    id: int 
    method: feedingMethod 
    time: datetime = Field(default_factory = datetime.now)
    amount_oz: Optional[int] = None
    amount_ml: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=200)


    @model_validator(mode="after")
    @classmethod
    def check_oz_and_ml(cls,values):
        oz = values.amount_oz
        ml = values.amount_ml

        # Check if either oz or ml is set, and ensure no negative values
        if oz is not None and oz < 0:
            raise ValueError("Amount_oz cannot be negative")
        if ml is not None and ml < 0:
            raise ValueError("Amount_ml cannot be negative")

        if oz > 32:
            raise ValueError("Amount_oz cannot be more than 32 ounces for a day")
        if ml > 950:
            raise ValueError("Amount_ml cannot be more than 950 ml for a day")

        # Ensure only one of oz or ml is non-zero
        if oz > 0 and ml:
            raise ValueError("Either amount_oz or amount_ml must be set, not both")

        # Ensure that at least one of oz or ml is set (not both 0)
        if oz == 0 and ml == 0:
            raise ValueError("Either amount_oz or amount_ml must be set")

        return values

    @field_validator("time",mode = 'before')
    @classmethod
    def time_can_not_be_in_future(cls,value):
        # Ensure `time` is not None
        if value is None:
            raise ValueError("Time cannot be None")

        if value > datetime.now():
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
