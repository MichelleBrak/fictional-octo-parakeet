import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Signup
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200 or response.status_code == 400  # 400 if already signed up
    # Unregister
    response = client.delete("/activities/Chess Club/unregister?email=tester@mergington.edu")
    assert response.status_code == 200 or response.status_code == 400  # 400 if not signed up

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/Programming Class/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_unregister_not_signed_up():
    response = client.delete("/activities/Gym Class/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert "not registered" in response.json().get("detail", "")
