from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.security import get_current_identity
from app.database.db import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker



TEST_DATABASE_URL = "postgresql+psycopg2://postgres:8911@localhost:8911/expense_test_db"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()


def override_get_current_identity():
    return 1

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_identity] = override_get_current_identity
client = TestClient(app)


@pytest.fixture
def setup_test_db():
    Base.metadata.create_all(bind = test_engine)
    yield
    Base.metadata.drop_all(bind =test_engine)


def test_create_expense_success(setup_test_db):

    response = client.post("/expenses/",
          json = { "title": "Lunch",
          "description": "Restaurant",
          "amount": 25.5,
           "date": "2026-05-07"
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 25.5
    assert data["user_id"] == 1
    assert data["date"] == "2026-05-07"


def  test_create_expense_missing_title(setup_test_db):

    response = client.post("/expenses/",
                           json = {
                               "description": "Restaurant",
                               "amount": 25.5,
                               "date": "2026-05-07"
                           }


                         )
    assert response.status_code == 422

def  test_create_expense_invalid_amount(setup_test_db):

    response = client.post("/expenses/",
                           json = {
                               "title": "Lunch",
                               "description": "Restaurant",
                               "amount": "not a number",
                               "date": "2026-05-07"
                           }


                         )
    assert response.status_code == 422
    data = response.json()



def test_get_expense_by_expense_id(setup_test_db):
    response = client.post(
        "/expenses/",
            json={
                "title": "Lunch",
                 "description": "Restaurant",
                 "amount": 40.0,
                  "date": "2026-05-07"
                 }
        )
    assert response.status_code == 201, response.text

    data = response.json()
    expense_id = data["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 40 or data["amount"] == 40.0
    assert data["user_id"] == 1


def test_get_expense_not_found(setup_test_db):


    response = client.get("/expenses/99")

    assert response.status_code == 404, response.text

    data = response.json()
    assert data["detail"] == "Expense not found"



def test_update_expense(setup_test_db):
    response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "description": "Restaurant",
            "amount": 40.0,
            "date": "2026-05-07"
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    expense_id = data["id"]
    assert data["title"] == "Lunch"
    assert data["description"] == "Restaurant"
    assert data["amount"] == 40.0

    response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "description": "Restaurant-Sushi",
            "amount": 60.0,
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "Lunch"  # unchanged
    assert data["description"] == "Restaurant-Sushi"
    assert data["amount"] == 60.0
    assert data["user_id"] == 1


def test_delete_expense(setup_test_db):
    response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "description": "Restaurant",
            "amount": 40.0,
            "date": "2026-05-07"
        }
    )
    assert response.status_code == 201, response.text

    data = response.json()
    expense_id = data["id"]
    assert data["id"] is not None


    response = client.delete(f"/expenses/{expense_id}"  )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["message"] == "Expense deleted successfully"

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 404, response.text

    data = response.json()
    assert data["detail"] == "Expense not found"









