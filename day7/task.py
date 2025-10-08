from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from contextlib import asynccontextmanager
from pydantic import BaseModel


DATABASE_URL = "sqlite:///books.db"
engine = create_engine(DATABASE_URL, echo=True)

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # auto-increment primary key
    title: str = Field(index=True, unique=True)             # book title must be unique
    author: str                                            # author name
    pages: int                                            # number of pages

#for book update model
class BookUpdate(BaseModel):
    title: str
    author: str
    pages: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # create tables if not exist
    yield

app = FastAPI(title="Book Manager API", lifespan=lifespan)

#Create Book
@app.post("/books")
def create_book(book: Book):
    with Session(engine) as session:
        # Check if a book with same title exists
        existing_book = session.exec(select(Book).where(Book.title == book.title)).first()

        if existing_book:
            # Replace existing book details
            existing_book.author = book.author
            existing_book.pages = book.pages
            session.add(existing_book)
            session.commit()
            session.refresh(existing_book)
            return {
                "message": f"Book '{book.title}' updated successfully",
                "book": existing_book
            }

        # If no duplicate, create new book
        session.add(book)
        session.commit()
        session.refresh(book)
        return {"message": "Book added successfully", "book": book}

#Get List of Books
@app.get("/books")
def list_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()  # fetch all books
        return {"books": books}


#Delete Book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"message": "Book deleted successfully"}

