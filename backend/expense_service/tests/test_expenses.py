from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.security import get_current_identity
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


def test_update_expense_not_found(setup_test_db):
    response = client.patch("/expenses/99", json={"amount": 10.0})
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Expense not found"


def test_delete_expense_not_found(setup_test_db):
    response = client.delete("/expenses/99")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Expense not found"


def test_create_expense_default_category(setup_test_db):
    response = client.post(
        "/expenses/",
        json={"title": "Lunch", "amount": 10.0, "date": "2026-05-07"},
    )
    assert response.status_code == 201, response.text
    assert response.json()["category"] == "Other"


def test_create_expense_with_category(setup_test_db):
    response = client.post(
        "/expenses/",
        json={"title": "Taxi", "amount": 12.0, "date": "2026-05-07", "category": "Transport"},
    )
    assert response.status_code == 201, response.text
    assert response.json()["category"] == "Transport"


def test_create_expense_invalid_category(setup_test_db):
    response = client.post(
        "/expenses/",
        json={"title": "Lunch", "amount": 10.0, "date": "2026-05-07", "category": "Pizza"},
    )
    assert response.status_code == 422, response.text


def _seed(category, date, title="x", amount=10.0):
    r = client.post(
        "/expenses/",
        json={"title": title, "amount": amount, "date": date, "category": category},
    )
    assert r.status_code == 201, r.text
    return r.json()


def test_list_returns_page_wrapper(setup_test_db):
    _seed("Food", "2026-05-01")
    _seed("Transport", "2026-05-02")

    response = client.get("/expenses/")
    assert response.status_code == 200, response.text
    data = response.json()

    # Shape: { items, total, limit, offset }
    assert set(data.keys()) == {"items", "total", "limit", "offset"}
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["limit"] == 20
    assert data["offset"] == 0


def test_list_filter_by_category(setup_test_db):
    _seed("Food", "2026-05-01")
    _seed("Food", "2026-05-02")
    _seed("Transport", "2026-05-03")

    response = client.get("/expenses/", params={"category": "Food"})
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["total"] == 2
    assert all(item["category"] == "Food" for item in data["items"])


def test_list_filter_by_date_range(setup_test_db):
    _seed("Food", "2026-05-01")
    _seed("Food", "2026-05-10")
    _seed("Food", "2026-05-20")

    response = client.get(
        "/expenses/", params={"start_date": "2026-05-05", "end_date": "2026-05-15"}
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["date"] == "2026-05-10"


def test_list_pagination(setup_test_db):
    for i in range(1, 6):
        _seed("Food", f"2026-05-0{i}")

    # First page of 2
    page1 = client.get("/expenses/", params={"limit": 2, "offset": 0}).json()
    assert page1["total"] == 5
    assert len(page1["items"]) == 2

    # Second page of 2
    page2 = client.get("/expenses/", params={"limit": 2, "offset": 2}).json()
    assert len(page2["items"]) == 2

    # Pages must not overlap
    ids1 = {item["id"] for item in page1["items"]}
    ids2 = {item["id"] for item in page2["items"]}
    assert ids1.isdisjoint(ids2)


def test_list_rejects_bad_limit(setup_test_db):
    # limit above the le=100 bound -> 422
    response = client.get("/expenses/", params={"limit": 9999})
    assert response.status_code == 422, response.text


def test_health_liveness():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_readiness():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"









