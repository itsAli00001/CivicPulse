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
    assert data["category"] == "water"
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

    
def test_update_complaint_status_to_in_progress():
    create_response = client.post(
        "/api/complaints",
        json={
            "text": "Street light is not working near our house.",
            "location": "Islamabad Sector G-10"
        }
    )
    complaint_id = create_response.json()["id"]

    response = client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_update_complaint_status_to_resolved():
    create_response = client.post(
        "/api/complaints",
        json={
            "text": "Garbage has not been collected for several days.",
            "location": "Islamabad Sector G-10"
        }
    )
    complaint_id = create_response.json()["id"]

    first_response = client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"status": "in_progress"}
    )
    assert first_response.status_code == 200

    response = client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"status": "resolved"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"


def test_reject_invalid_status_transition():
    create_response = client.post(
        "/api/complaints",
        json={
            "text": "There is a damaged road near our street.",
            "location": "Islamabad Sector G-10"
        }
    )
    complaint_id = create_response.json()["id"]

    response = client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"status": "resolved"}
    )

    assert response.status_code == 409
    assert response.json()["detail"]


def test_update_status_for_missing_complaint():
    missing_id = "00000000-0000-0000-0000-000000000000"

    response = client.patch(
        f"/api/complaints/{missing_id}/status",
        json={"status": "in_progress"}
    )

    assert response.status_code == 404


def test_reject_unknown_status():
    create_response = client.post(
        "/api/complaints",
        json={
            "text": "There is a damaged road near our street.",
            "location": "Islamabad Sector G-10"
        }
    )
    complaint_id = create_response.json()["id"]

    response = client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"status": "pending"}
    )

    assert response.status_code == 422
