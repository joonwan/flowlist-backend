from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "study fastapi",
            "description": "write api tests",
            "priority": 2,
            "due_date": "2026-05-12",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "study fastapi"
    assert data["description"] == "write api tests"
    assert data["priority"] == 2
    assert data["due_date"] == "2026-05-12"
    assert data["is_done"] is False

def test_create_task_validation_error():
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "priority": 10,
        }
    )
    
    assert response.status_code == 422