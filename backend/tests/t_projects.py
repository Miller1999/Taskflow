from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_project():
    response = client.post(
        "/projects/",
        json={
            "name": "Mi Proyecto",
            "description": "Descripción del proyecto",
            "user_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Mi Proyecto"
