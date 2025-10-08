from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from contextlib import asynccontextmanager
from pydantic import BaseModel


DATABASE_URL = "sqlite:///crud.db"  # SQLite file named crud.db
db_engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL queries

class TaskUpdate(BaseModel):
    title: str
    completed: bool

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # primary key auto-increment
    title: str = Field(index=True, unique=True)                                         # task title
    completed: bool = Field(default=False)                 # task status

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(db_engine)  # creates tables if they don't exist
    yield                                 # run the app

app = FastAPI(title="Mini CRUD API", lifespan=lifespan)

# Create Task or Replace if Duplicate
@app.post("/task")
def create_task(task: Task):
    with Session(db_engine) as session:
        # Check if a task with the same title exists
        existing_task = session.exec(select(Task).where(Task.title == task.title)).first()

        if existing_task:
            # Replace existing task's data
            existing_task.completed = task.completed
            session.add(existing_task)
            session.commit()
            session.refresh(existing_task)
            return {
                "message": "Task updated successfully",
                "task": existing_task
            }

        # If no duplicate, create a new task
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "Task added successfully", "task": task}


#Get Task List
@app.get("/tasks")
def list_tasks():
    with Session(db_engine) as session:
        tasks = session.exec(select(Task)).all()  # select all tasks
        return {"tasks": tasks}

#Get Task By id
@app.get("/task/{task_id}")
def get_task(task_id: int):
    with Session(db_engine) as session:
        task = session.get(Task, task_id)  # get task by primary key
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task": task}

# For Update Task
@app.put("/task/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    with Session(db_engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.title = updated_task.title
        task.completed = updated_task.completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "Task updated successfully", "task": task}

#Delete Task
@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    with Session(db_engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}, 200

