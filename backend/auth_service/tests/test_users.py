from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database.db import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker


TEST_DATABASE_URL = "postgresql+psycopg2://postgres:8911@localhost:8911/expense_test_db"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)
client = TestClient(app)

# def override_get_db():
#         session = TestingSessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()

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
