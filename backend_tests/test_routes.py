from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from backend.main import app
from backend.schemas import FeedEntry,FeedEntryResponse
from backend.database import create_db_and_tables,get_session
from backend.enums import feedingMethod
from datetime import datetime
from sqlmodel import Session, delete
from backend.models import FeedingDBModel
import pytest 

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    create_db_and_tables()

@pytest.fixture(autouse=True)
def clear_feedings():
    session = next(get_session())
    session.exec(delete(FeedingDBModel))
    session.commit()

def test_root_request():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Baby Feeding Application"};

def test_create_feed_request():
    feed= FeedEntry(
        method="breastfeeding",
        amount_oz=3,
        notes="Morning feed successful",
    )
    response = client.post("/createfeed/",json=jsonable_encoder(feed))
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None

def test_get_feed_with_data_request():
    # Create a feed 
    feed= FeedEntry(
        method="breastfeeding",
        amount_ml=60,
        notes="Morning feed successful",
    )
    response = client.post("/createfeed/",json=jsonable_encoder(feed))
    feed = response.json()
    feed_id = feed["id"]
    #print(data)

    # Get feed
    get_response = client.get(f"/getfeed/{feed_id}")
    get_response_data = get_response.json()

    assert get_response.status_code == 200
    assert get_response_data["method"] == feed["method"]
    assert get_response_data["amount_oz"] == 2.0
    assert get_response_data["notes"] == feed["notes"]

def test_get_feed_without_data_request():
    get_response = client.get(f"/getfeed/{2019}")
    get_response_data = get_response.json()

    assert get_response.status_code == 404
    assert get_response_data["detail"] == "Feeding not found"
    
def test_get_feedings_filter_by_method_request():
    feed1 = FeedEntry(method="food", amount_oz=5, amount_ml=0, notes="food feed")
    feed2 = FeedEntry(method="bottle", amount_oz=3, amount_ml=0, notes="bottle feed")

    client.post("/createfeed/", json=jsonable_encoder(feed1))
    client.post("/createfeed/", json=jsonable_encoder(feed2))

    response = client.get("/getfeedings?method=food")
    data = response.json()

    assert response.status_code == 200
    assert all(feed["method"] == "food" for feed in data)
    
def test_get_feedings_filter_by_oz_request():
    feed1 = FeedEntry(method="food", amount_oz=5, amount_ml=0, notes="food feed")
    feed2 = FeedEntry(method="bottle", amount_oz=3, amount_ml=0, notes="bottle feed")
    feed3 = FeedEntry(method="bottle", amount_oz=12, amount_ml=0, notes="bottle feed")
    feed4 = FeedEntry(method="bottle", amount_oz=9, amount_ml=0, notes="bottle feed")

    client.post("/createfeed/", json=jsonable_encoder(feed1))
    client.post("/createfeed/", json=jsonable_encoder(feed2))
    client.post("/createfeed/", json=jsonable_encoder(feed3))
    client.post("/createfeed/", json=jsonable_encoder(feed4))

    response = client.get("/getfeedings?min_oz=3&max_oz=9")
    data = response.json()

    assert response.status_code == 200
    assert all(feed["amount_oz"] >= 3 for feed in data) 

def test_get_feedings_filter_by_time_request():
    feed1 = FeedEntry(method="food", amount_oz=5, time=datetime(2025, 9, 10, 8, 30), notes="morning")
    feed2 = FeedEntry(method="bottle", amount_oz=3, time=datetime(2025, 9, 10, 13, 0), notes="afternoon")
    feed3 = FeedEntry(method="bottle", amount_oz=3, time=datetime(2025, 8, 10, 13, 0), notes="afternoon")
    feed4 = FeedEntry(method="bottle", amount_oz=4, time=datetime(2025, 8, 10, 8, 0), notes="morning")

    client.post("/createfeed/", json=jsonable_encoder(feed1))
    client.post("/createfeed/", json=jsonable_encoder(feed2))
    client.post("/createfeed/", json=jsonable_encoder(feed3))
    client.post("/createfeed/", json=jsonable_encoder(feed4))

    response = client.get("/getfeedings?start_datetime=2025-08-10T08:00:00&end_datetime=2025-09-10T12:00:00")
    data = response.json()

    feeds = [FeedEntryResponse(**f) for f in data]
    assert all(datetime(2025, 8, 10, 8, 0) <= f.time <= datetime(2025, 9, 10, 12, 0) for f in feeds)

def test_get_feedings_with_data_request():
    # Arrange: create some feeds
    feed1 = FeedEntry(method="food", amount_oz=5, notes="food feed")
    feed2 = FeedEntry(method="bottle", amount_oz=3, notes="bottle feed")

    client.post("/createfeed/", json=jsonable_encoder(feed1))
    client.post("/createfeed/", json=jsonable_encoder(feed2))

    # Act: request feedings
    response = client.get("/getfeedings")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(feed["method"] == "food" for feed in data)
    assert any(feed["method"] == "bottle" for feed in data)

def test_get_feedings_without_data_request():
     # Act: request feedings without creating any
    response = client.get("/getfeedings")
    data = response.json()
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "There are no feedings found"

def test_delete_feeding_with_data_request():
    # Create a feed 
    feed= FeedEntry(
        method="breastfeeding",
        amount_ml=60,
        notes="Morning feed successful",
    )
    response = client.post("/createfeed/",json=jsonable_encoder(feed))
    feed = response.json()
    feed_id = feed["id"]

    delete_response = client.delete(f"/deletefeed/{feed_id}")
    delete_response_data = delete_response.json()

    assert delete_response.status_code == 200
    assert delete_response_data["ok"] == True

def test_delete_feeding_with_out_data_request():
    response = client.delete(f"/deletefeed/{2031}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Feeding can not be found"
    
def test_delete_feedings_with_data_request():
    # Create a feed 
    feed1= FeedEntry(method="breastfeeding",amount_ml=60,notes="Morning feed successful")
    feed2= FeedEntry(method="bottle",amount_oz=5)
    feed3= FeedEntry(method="food",amount_oz=10,notes="success") 

    response1 = client.post("/createfeed/",json=jsonable_encoder(feed1))
    response2 = client.post("/createfeed/",json=jsonable_encoder(feed2))
    response3 = client.post("/createfeed/",json=jsonable_encoder(feed3))
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200

    response = client.delete("/deletefeedings")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "All feedings deleted"

def test_delete_feedings_without_data_request():
    response = client.delete("/deletefeedings")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There are no feedings found"

def test_patch_feeding_with_data_request():
    # Create feed entry
    feed = FeedEntry(method="food",amount_oz=10,notes="success") 
    create_response = client.post("/createfeed/",json=jsonable_encoder(feed))
    data = create_response.json()
    feed_id = data["id"]

    # Updated feed
    update_feed = FeedEntry(method="bottle",amount_oz=10,notes="success") 

    update_response = client.put(f"/updatefeedings/{feed_id}",json=jsonable_encoder(update_feed))
    update_data = update_response.json()

    assert update_response.status_code == 200
    assert update_data["message"] == "Feed has been updated"

    get_response = client.get("/getfeedings")
    feeds = get_response.json()

    updated = next((f for f in feeds if f["id"] == feed_id), None)
    assert updated is not None
    assert updated["method"] == "bottle"
    assert updated["amount_oz"] == 10
    assert updated["notes"] == "success"

def test_patch_feeding_without_data_request():
    feed = FeedEntry(method="food",amount_oz=10,notes="success") 
    response = client.put(f"/updatefeedings/{23}",json=jsonable_encoder(feed))
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Feeding not found"
