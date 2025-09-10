from fastapi import APIRouter, Depends, HTTPException, Query
from backend.schemas import FeedEntry, FeedEntryID,FeedEntryResponse
from backend.database import get_session  
from backend.models import FeedingDBModel
from sqlmodel import Session,select,delete
from datetime import datetime
from typing import Optional 
from backend.enums import feedingMethod

router = APIRouter()

fakefeeds = {}

@router.get("/")
async def root():
    return {"message": "Hello Baby Feeding Application"}

# Create a feeding
@router.post("/createfeed/", response_model=FeedEntryResponse)
async def create_feed(feeding: FeedEntry, session: Session = Depends(get_session))-> FeedEntryID:
    db_feed = FeedingDBModel(**feeding.model_dump())
    
    session.add(db_feed)
    session.commit()
    session.refresh(db_feed)

    print({"message": "Feeding created"})
    return FeedEntryResponse.from_db(db_feed)

# Get a feeding
@router.get("/getfeed/{feedID}", response_model=FeedEntryResponse)
async def get_feed(feedID: int, session: Session = Depends(get_session)):
    statement = select(FeedingDBModel).where(FeedingDBModel.id == feedID)
    feed = session.exec(statement).first()

    if not feed:
        raise HTTPException(status_code=404, detail="Feeding not found")

    return FeedEntryResponse.from_db(feed)

# Get all feedings filtered or not
@router.get("/getfeedings")
async def get_feedings(
    method: Optional[feedingMethod] = Query(None),
    min_oz: Optional[float] = Query(None),
    max_oz: Optional[float] = Query(None),
    start_datetime: Optional[datetime] = Query(None),
    end_datetime: Optional[datetime] = Query(None),
    session: Session = Depends(get_session)
):
    query = select(FeedingDBModel)

    if method:
        query = query.where(FeedingDBModel.method == method)
    if min_oz is not None:
        query = query.where(FeedingDBModel.amount_oz >= min_oz)
    if max_oz is not None:
        query = query.where(FeedingDBModel.amount_oz <= max_oz)
    if start_datetime is not None:
        query = query.where(FeedingDBModel.time >= start_datetime)
    if end_datetime is not None:
        query = query.where(FeedingDBModel.time <= end_datetime)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="There are no feedings found")

    return results

# Delete a feeding
@router.delete("/deletefeed/{feedID}")
async def delete_feed(feedID: int, session: Session = Depends(get_session)):
    feeding = session.get(FeedingDBModel, feedID)
    if not feeding:
        raise HTTPException(status_code=404, detail="Feeding can not be found")
    session.delete(feeding)
    session.commit()
    return {"ok": True}

# Delete all feedings
@router.delete("/deletefeedings")
async def delete_feedings(session: Session = Depends(get_session)):
    try:
        feedings = session.exec(select(FeedingDBModel)).all()

        if not feedings:
            raise HTTPException(status_code=404, detail="There are no feedings found")

        session.exec(delete(FeedingDBModel))
        session.commit()

        return {"message": "All feedings deleted"}

    except HTTPException:
        raise

    except Exception as e:
        print("Unexpected error while deleting feedings:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

# Update feeding
@router.put("/updatefeedings/{feedID}")
async def update_feed(feedID: int, update_feed: FeedEntry, session: Session = Depends(get_session)):
    feed = session.get(FeedingDBModel,feedID)

    if not feed:
        raise HTTPException(status_code=404, detail="Feeding not found")

    feed.method = update_feed.method
    feed.time = update_feed.time
    feed.amount_oz = update_feed.amount_oz
    feed.notes = update_feed.notes

    session.add(feed)
    session.commit()
    session.refresh(feed)

    return {"message": "Feed has been updated"}


