import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, Base, get_db
from app.database import SQLALCHEMY_DATABASE_URL
from app import models

# Use a separate in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_task():
    payload = {"title": "Test task", "description": "desc"}
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert "id" in data
    assert data["status"] == "created"


def test_get_task_not_found():
    resp = client.get("/tasks/non-existent-id")
    assert resp.status_code == 404


def test_list_tasks_and_pagination():
    for i in range(5):
        client.post("/tasks", json={"title": f"t{i}"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 5

    resp2 = client.get("/tasks?skip=2&limit=2")
    assert resp2.status_code == 200
    assert len(resp2.json()) == 2


def test_update_task():
    create = client.post("/tasks", json={"title": "to update", "description": "old"})
    tid = create.json()["id"]
    update_payload = {"title": "updated", "status": "in_progress"}
    resp = client.put(f"/tasks/{tid}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "updated"
    assert data["status"] == "in_progress"


def test_delete_task():
    create = client.post("/tasks", json={"title": "to delete"})
    tid = create.json()["id"]
    resp = client.delete(f"/tasks/{tid}")
    assert resp.status_code == 204

    resp_get = client.get(f"/tasks/{tid}")
    assert resp_get.status_code == 404


def test_invalid_status_on_update():
    create = client.post("/tasks", json={"title": "status test"})
    tid = create.json()["id"]
    resp = client.put(f"/tasks/{tid}", json={"status": "invalid_status"})
    assert resp.status_code == 422
