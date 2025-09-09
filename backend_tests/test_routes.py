from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from backend.main import app
from backend.schemas import FeedEntry,FeedEntryResponse
from backend.database import create_db_and_tables
import pytest 

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    create_db_and_tables()

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

"""	
def test_get_feeding_request():
	 feed= FeedEntry(
		method="breastfeeding",
		amount_oz=20,
		notes="Morning feed successful",
	)
	response = client.post("/feeding",json=feed.model_dump())
	data = response.json()
	feed_id = data["id"]
	#assert response.status_code == 200
	
	get_response = client.get(f"/getfeed{feed_id}")
	get_data = get_response.json()
	
	#assert get_response.status_code == 200
	#assert get_data["id"] == feed_id
	pass

def test_get_feedings_request():
	#response = client.get():
	pass

def test_delete_feeding_request():
	#response = client.get():
	pass

def test_delete_feedings_request():
	#response = client.get():
	pass

def test_patch_feeding_request():
	#response = client.get():
	pass
"""
