import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    activity = "Soccer Team"
    name = "Test User"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Signup
    response = client.post(f"/activities/{activity}/signup", json={"name": name, "email": email})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", json={"name": name, "email": email})
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404

def test_all_activities_exist_and_valid():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    expected_activities = [
        "Soccer Team",
        "Basketball Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Olympiad",
        "Chess Club",
        "Programming Class",
        "Gym Class"
    ]
    for activity in expected_activities:
        assert activity in data, f"{activity} missing in activities list"
        details = data[activity]
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert isinstance(details["participants"], list)
        # Check that no participant is missing name or email
        for p in details["participants"]:
            assert "name" in p and p["name"], f"Missing name in {activity} participant"
            assert "email" in p and p["email"], f"Missing email in {activity} participant"
