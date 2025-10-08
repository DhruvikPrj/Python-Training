# day4/test_task.py
import pytest
from fastapi.testclient import TestClient
from day4.task import app  # Make sure day4 has __init__.py to be treated as a package

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# ----------------------------
# Test GET /hello
# ----------------------------
def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200  # Check response code
    assert response.json() == {"message": "Hello, FastAPI!"}  # Check returned JSON

# ----------------------------
# Test POST /echo with valid message
# ----------------------------
def test_echo():
    payload = {"message": "Hello World"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == {"echo": "Hello World"}

# ----------------------------
# Test POST /echo with empty string
# ----------------------------
def test_echo_empty():
    payload = {"message": ""}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == {"echo": ""}

# ----------------------------
# Test POST /echo missing field (should raise validation error)
# ----------------------------
def test_echo_missing_field():
    payload = {}  # "message" field missing
    response = client.post("/echo", json=payload)
    assert response.status_code == 422  # Pydantic validation error
