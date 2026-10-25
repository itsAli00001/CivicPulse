from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_complaint():
    response = client.post(
        "/api/complaints",
        json={
            "text": "There is a broken water pipe near our street.",
            "location": "Islamabad Sector G-10",
            "reporter_contact": "03001234567"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["category"] == "other"
    assert data["priority"] == "normal"
    assert data["status"] == "open"
    assert data["triaged_by"] == "rules"


def test_get_complaint():
    create_response = client.post(
        "/api/complaints",
        json={
            "text": "There is a broken water pipe near our street.",
            "location": "Islamabad Sector G-10"
        }
    )

    assert create_response.status_code == 200

    complaint_id = create_response.json()["id"]

    response = client.get(f"/api/complaints/{complaint_id}")

    assert response.status_code == 200
    assert response.json()["id"] == complaint_id


def test_get_complaints():
    response = client.get("/api/complaints")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_reporter_contact():
    response = client.post(
        "/api/complaints",
        json={
            "text": "There is a broken water pipe near our street.",
            "location": "Islamabad Sector G-10",
            "reporter_contact": "12345"
        }
    )

    assert response.status_code == 422


def test_valid_reporter_contact():
    response = client.post(
        "/api/complaints",
        json={
            "text": "There is a broken water pipe near our street.",
            "location": "Islamabad Sector G-10",
            "reporter_contact": "03001234567"
        }
    )

    assert response.status_code == 200