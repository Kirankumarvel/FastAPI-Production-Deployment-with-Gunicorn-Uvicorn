import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    item_data = {"name": "Test Item", "price": 9.99}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
    assert "id" in response.json()

def test_get_item():
    # First create an item
    item_data = {"name": "Test Item", "price": 9.99}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_get_nonexistent_item():
    response = client.get("/items/nonexistent")
    assert response.status_code == 404

def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)