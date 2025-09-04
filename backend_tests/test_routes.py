from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.main import app

client = TestClient(app)

def test_root_request():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello Baby Feeding Application"};

def test_create_feed_request():
	response = client.post("/feeding")
	pass

def test_get_feeding_request():
	#response = client.get():
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

