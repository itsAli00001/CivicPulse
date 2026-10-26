from app.cache.redis_client import invalidate_statistics_cache
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_complaint(text, location="Islamabad Sector G-10"):
    response = client.post(
        "/api/complaints",
        json={
            "text": text,
            "location": location
        }
    )
    assert response.status_code == 200
    return response.json()


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
    complaint = create_test_complaint(
        "There is a broken water pipe near our street."
    )

    response = client.get(
        f"/api/complaints/{complaint['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == complaint["id"]


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
    complaint = create_test_complaint(
        "Street light is not working near our house."
    )

    response = client.patch(
        f"/api/complaints/{complaint['id']}/status",
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_update_complaint_status_to_resolved():
    complaint = create_test_complaint(
        "Garbage has not been collected for several days."
    )

    first_response = client.patch(
        f"/api/complaints/{complaint['id']}/status",
        json={"status": "in_progress"}
    )

    assert first_response.status_code == 200

    response = client.patch(
        f"/api/complaints/{complaint['id']}/status",
        json={"status": "resolved"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"


def test_reject_invalid_status_transition():
    complaint = create_test_complaint(
        "There is a damaged road near our street."
    )

    response = client.patch(
        f"/api/complaints/{complaint['id']}/status",
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
    complaint = create_test_complaint(
        "There is a damaged road near our street."
    )

    response = client.patch(
        f"/api/complaints/{complaint['id']}/status",
        json={"status": "pending"}
    )

    assert response.status_code == 422


def test_filter_complaints_by_status():
    complaint = create_test_complaint(
        "Street light is not working near our house."
    )

    response = client.get(
        "/api/complaints?status=open"
    )

    assert response.status_code == 200
    assert all(
        item["status"] == "open"
        for item in response.json()
    )

    assert any(
        item["id"] == complaint["id"]
        for item in response.json()
    )


def test_filter_complaints_by_category():
    complaint = create_test_complaint(
        "There is a broken water pipe near our street."
    )

    response = client.get(
        "/api/complaints?category=water"
    )

    assert response.status_code == 200
    assert all(
        item["category"] == "water"
        for item in response.json()
    )

    assert any(
        item["id"] == complaint["id"]
        for item in response.json()
    )


def test_limit_complaints():
    for index in range(3):
        create_test_complaint(
            f"There is a broken water pipe near street number {index}."
        )

    response = client.get(
        "/api/complaints?limit=2"
    )

    assert response.status_code == 200
    assert len(response.json()) <= 2


def test_offset_complaints():
    for index in range(3):
        create_test_complaint(
            f"There is a broken water pipe near street number {index}."
        )

    first_page = client.get(
        "/api/complaints?limit=2&offset=0"
    )

    second_page = client.get(
        "/api/complaints?limit=2&offset=2"
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200

    first_ids = {
        item["id"]
        for item in first_page.json()
    }

    second_ids = {
        item["id"]
        for item in second_page.json()
    }

    assert first_ids.isdisjoint(second_ids)


def test_reject_invalid_pagination_values():
    response = client.get(
        "/api/complaints?limit=0"
    )

    assert response.status_code == 422

    response = client.get(
        "/api/complaints?offset=-1"
    )

    assert response.status_code == 422


def test_get_statistics():
    invalidate_statistics_cache()

    response = client.get("/api/statistics")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "by_category" in data
    assert "by_status" in data

    assert isinstance(data["total"], int)
    assert isinstance(data["by_category"], dict)
    assert isinstance(data["by_status"], dict)

    invalidate_statistics_cache()


def test_statistics_cache():
    invalidate_statistics_cache()

    first_response = client.get("/api/statistics")

    assert first_response.status_code == 200
    assert first_response.headers.get("x-cache") == "MISS"

    second_response = client.get("/api/statistics")

    assert second_response.status_code == 200
    assert second_response.headers.get("x-cache") == "HIT"

    assert first_response.json() == second_response.json()

    invalidate_statistics_cache()