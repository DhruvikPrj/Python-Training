import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from day7.task import app, Book, engine  # replace book_app with your file name

# Use TestClient with lifespan support
client = TestClient(app)

@pytest.fixture(name="db_session")
def session_fixture():
    # Setup: create tables
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Teardown: drop tables after test.sh
    SQLModel.metadata.drop_all(engine)

def test_create_book(db_session):
    # Create a new book
    response = client.post("/books", json={
        "title": "Test Book",
        "author": "John Doe",
        "pages": 123
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] in ["Book added successfully", "Book 'Test Book' updated successfully"]
    assert data["book"]["title"] == "Test Book"
    assert data["book"]["author"] == "John Doe"
    assert data["book"]["pages"] == 123

def test_update_book(db_session):
    # First, create a book
    client.post("/books", json={"title": "Update Book", "author": "Alice", "pages": 50})

    # Now, update the same book
    response = client.post("/books", json={"title": "Update Book", "author": "Bob", "pages": 75})
    assert response.status_code == 200
    data = response.json()
    assert "updated successfully" in data["message"]
    assert data["book"]["author"] == "Bob"
    assert data["book"]["pages"] == 75

def test_list_books(db_session):
    # Add some books
    client.post("/books", json={"title": "Book 1", "author": "Author 1", "pages": 10})
    client.post("/books", json={"title": "Book 2", "author": "Author 2", "pages": 20})

    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    titles = [b["title"] for b in data["books"]]
    assert "Book 1" in titles
    assert "Book 2" in titles

def test_delete_book(db_session):
    # Add a book to delete
    create_resp = client.post("/books", json={"title": "Delete Me", "author": "Author X", "pages": 99})
    book_id = create_resp.json()["book"]["id"]

    # Delete it
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Book deleted successfully"

    # Confirm deletion
    response = client.get("/books")
    books = [b["title"] for b in response.json()["books"]]
    assert "Delete Me" not in books

def test_delete_nonexistent_book(db_session):
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
