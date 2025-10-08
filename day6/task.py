from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, select, create_engine
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite:///todo.db"
engine = create_engine(DATABASE_URL, echo=True)

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)

# Lifespan context to run startup and shutdown code
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables when the app starts
    SQLModel.metadata.create_all(engine)
    yield  # app runs normally after this

app = FastAPI(title="To-Do API", lifespan=lifespan)

@app.post("/task")
def create_task(task: Task):
    with Session(engine) as session:
        existing_task = session.exec(select(Task).where(Task.title == task.title)).first()
        if existing_task:
            # Update the existing task
            existing_task.completed = task.completed
            existing_task.title = task.title
            session.add(existing_task)
            session.commit()
            session.refresh(existing_task)
            return {"message": "Task updated successfully", "task": existing_task}

        # Create a new task
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "Task created successfully", "task": task}

@app.get("/tasks")
def list_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return {"message": "Task list retrieved successfully", "tasks": tasks}
