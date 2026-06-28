from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database.db import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:test_password@localhost:8911/test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Route DB access to the test engine so tests never touch the real database.
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def setup_test_db():
    Base.metadata.create_all(bind = test_engine)
    yield
    Base.metadata.drop_all(bind =test_engine)

def test_register_user(setup_test_db):
    response = client.post(
        "/users/",
        json={
            "first_name": "Jasper",
            "email": "jasper@test.com",
            "password": "89112077"
        }
    )

    assert response.status_code == 201, response.text
    data = response.json()

    assert data["email"] == "jasper@test.com"
    assert data["first_name"] == "Jasper"
    assert "user_id" in data

def test_login(setup_test_db):

    client.post(
        "/users/",
        json={
            "first_name": "Jasper",
            "email": "jasper@test.com",
            "password": "89112077"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "jasper@test.com",
            "password": "89112077"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_health_liveness():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_readiness():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
