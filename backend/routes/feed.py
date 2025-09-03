from fastapi import APIRouter
from backend.schemas import FeedEntry 

router = APIRouter()

fakefeeds = {}

@router.get("/")
async def root():
    return {"message": "Hello Baby Feeding Application"}

# Create a feeding
@router.post("/feedings/")
async def createFeed(feeding: FeedEntry):
    fakefeeds[feeding.id] = feeding.model_dump()
    return {"message": "Feeding created"}

# Get a feeding
@router.get("/feeding/{feedID}")
async def root(feedID: int):
    if feedID in fakefeeds:
        return {"message": "Get feeding"}
    raise HTTPException(status_code=404, detail= "Feed can not be found")

# Get all feedings
@router.get("/feedings")
async def Getfeedings():
    if fakefeeds: 
        return fakefeeds
    raise HTTPException(status_code=404, detail= "There are no feedings")

# Delete a feeding
@router.delete("/delete/feeding")
async def root(feedID: int):
    if fakefeeds(feedID):
        fakefeeds.pop(feedID)
        return {"message":  "Feeding deleted"}
    raise HTTPException(status_code=404, detail= "Feeding can not be found")

# Delete all feedings
@router.delete("/delete/feedings")
async def root():
    if fakefeeds:
        fakefeeds.clear()
        return {"message": "All feedings deleted"}
    raise HTTPException(status_code=404, detail= "There are no feedings to be found")
