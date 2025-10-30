import pytest
from fastapi.testclient import TestClient
from day6.task import app, engine, SQLModel, Task

# Use TestClient to run tests
client = TestClient(app)

# Run before each test.sh: recreate tables
@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def test_create_task():
    # Test creating a new task
    response = client.post("/task", json={"title": "Test Task", "completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task created successfully"
    assert data["task"]["title"] == "Test Task"
    assert data["task"]["completed"] is False

def test_update_task():
    # First create the task
    client.post("/task", json={"title": "Update Task", "completed": False})

    # Then update the same task
    response = client.post("/task", json={"title": "Update Task", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task updated successfully"
    assert data["task"]["title"] == "Update Task"
    assert data["task"]["completed"] is True

def test_list_tasks():
    # Create two tasks
    client.post("/task", json={"title": "Task 1", "completed": False})
    client.post("/task", json={"title": "Task 2", "completed": True})

    # Retrieve task list
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task list retrieved successfully"
    assert len(data["tasks"]) == 2
    titles = [task["title"] for task in data["tasks"]]
    assert "Task 1" in titles
    assert "Task 2" in titles
