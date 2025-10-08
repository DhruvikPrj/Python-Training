import json
import pytest
from fastapi.testclient import TestClient
from day5.task import app
client = TestClient(app)

# -----------------------------
# Helper: Read JSON file
# -----------------------------
def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


# -----------------------------
# Test POST /user → add new user
# -----------------------------
def test_create_user_add(tmp_path):
    # Use a temporary file for users.json
    users_file = tmp_path / "users.json"

    # Monkeypatch os.getcwd to tmp_path
    app.dependency_overrides = {}
    import os
    os_getcwd_original = os.getcwd
    os.getcwd = lambda: tmp_path

    payload = {"name": "Alice", "age": 25}
    response = client.post("/user/", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "User added successfully"
    assert response.json()["user"]["name"] == "Alice"

    # Check file content
    data = read_json_file(users_file)
    assert data[0]["name"] == "Alice"

    # Restore os.getcwd
    os.getcwd = os_getcwd_original


# -----------------------------
# Test POST /user → update existing user
# -----------------------------
def test_create_user_update(tmp_path):
    users_file = tmp_path / "users.json"
    os_getcwd_original = __import__("os").getcwd
    __import__("os").getcwd = lambda: tmp_path

    # Pre-populate file with a user
    with open(users_file, "w") as f:
        json.dump([{"name": "Bob", "age": 30}], f)

    payload = {"name": "Bob", "age": 35}  # updated age
    response = client.post("/user/", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["user"]["age"] == 35

    data = read_json_file(users_file)
    assert data[0]["age"] == 35

    # Restore os.getcwd
    __import__("os").getcwd = os_getcwd_original


# -----------------------------
# Test GET /user/{name} → user exists
# -----------------------------
def test_get_user_exists(tmp_path):
    users_file = tmp_path / "users.json"
    os_getcwd_original = __import__("os").getcwd
    __import__("os").getcwd = lambda: tmp_path

    # Pre-populate file
    with open(users_file, "w") as f:
        json.dump([{"name": "Charlie", "age": 40}], f)

    response = client.get("/user/Charlie")
    assert response.status_code == 200
    assert response.json()["user"]["age"] == 40

    __import__("os").getcwd = os_getcwd_original


# -----------------------------
# Test GET /user/{name} → user not found
# -----------------------------
def test_get_user_not_found(tmp_path):
    import os
    os_getcwd_original = os.getcwd
    os.getcwd = lambda: tmp_path  # point API to tmp folder

    # Case 1: File does NOT exist → should return "No users found"
    response = client.get("/user/Unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "No users found"

    # Case 2: File exists but user not in file
    users_file = tmp_path / "users.json"
    with open(users_file, "w") as f:
        json.dump([{"name": "Alice", "age": 25}], f)

    response = client.get("/user/Unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with name 'Unknown' not found"

    # Restore os.getcwd
    os.getcwd = os_getcwd_original

