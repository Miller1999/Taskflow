import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Asegúrate de que 'app' esté importado correctamente
from backend.database import SessionLocal, Base, engine
from backend import models
from backend.routers.auth import get_db

client = TestClient(app)


# Configuración de la base de datos de prueba
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_database():
    """Inicializa la base de datos de prueba."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(setup_database):
    """Prueba la creación de un usuario nuevo."""
    response = client.post(
        "/auth/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201


def test_login_user(setup_database):
    """Prueba el login de un usuario existente y la generación de un token."""
    # Crear usuario antes de intentar iniciar sesión
    client.post(
        "/auth/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )

    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
