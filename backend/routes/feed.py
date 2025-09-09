from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import FeedEntry, FeedEntryID
from backend.database import get_session  
from backend.models import FeedingDBModel
from sqlmodel import Session,select,delete

router = APIRouter()

fakefeeds = {}

@router.get("/")
async def root():
    return {"message": "Hello Baby Feeding Application"}

# Create a feeding
@router.post("/createfeed/", response_model=FeedEntryID)
async def create_feed(feeding: FeedEntry, session: Session = Depends(get_session))-> FeedEntryID:
    # Create ORM instance from Pydantic input
    db_feed = FeedingDBModel(**feeding.dict())
    
    session.add(db_feed)
    session.commit()
    session.refresh(db_feed)

    print({"message": "Feeding created"})
    return FeedEntryID(id=db_feed.id)

# Get a feeding
@router.get("/getfeed/{feedID}")
async def get_feed(feedID: int, session: Session = Depends(get_session)):
    statement = select(FeedingDBModel).where(FeedingDBModel.id == feedID)
    feed = session.exec(statement).first()

    if not feed:
        raise HTTPException(status_code=404, detail="Feeding not found")

    return feed

# Get all feedings
@router.get("/getfeedings")
async def get_feedings(session: Session = Depends(get_session)):
    results = session.exec(select(FeedingDBModel))
    feedings = results.all()

    if not feedings:
        raise HTTPException(status_code=404, detail="There are no feedings found")

    return feedings

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


