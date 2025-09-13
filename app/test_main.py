import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Production Deployment"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_detailed_health_check():
    response = client.get("/health/detailed")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "memory_usage_mb" in response.json()