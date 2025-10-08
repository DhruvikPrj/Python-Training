from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError

# Database setup
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, echo=True)


# Define User model
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Creating database and tables...")
    SQLModel.metadata.create_all(engine)
    yield
    print("🛑 Shutting down...")


# Attach lifespan to app
app = FastAPI(title="User API with SQLite", lifespan=lifespan)


# POST /user → Create user
@app.post("/user")
def create_user(user: User):
    try:
        with Session(engine) as session:
            # Check if user with same name already exists
            existing_user = session.exec(select(User).where(User.name == user.name)).first()
            if existing_user:
                # Option 1: replace old user
                existing_user.age = user.age
                session.add(existing_user)
                session.commit()
                session.refresh(existing_user)
                return {"message": "User updated successfully", "user": existing_user}

                # Option 2: Uncomment below if you want to prevent duplicates instead
                # raise HTTPException(status_code=400, detail=f"User '{user.name}' already exists")

            # If new user, add to DB
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"message": "User created successfully", "user": user}

    except IntegrityError as e:
        # Catch SQL errors (like primary key conflicts)
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


# GET /user/{name} → Fetch user by name
@app.get("/user/{name}")
def get_user(name: str):
    try:
        with Session(engine) as session:
            statement = select(User).where(User.name == name)
            result = session.exec(statement).first()
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            return {"message": "User Retrived successfully", "user": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
