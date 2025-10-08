import json
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


app = FastAPI(title="User API")

class User(BaseModel):
    name: str
    age: int

# For Store User Temporary
users_db = {}


@app.post("/user/")
async def create_user(user: User):
    file_path = os.path.join(os.getcwd(), "users.json")

    # Load existing users (if file exists)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    # ✅ Check if user exists → replace it
    updated = False
    for idx, existing_user in enumerate(users):
        if existing_user.get("name") == user.name:
            users[idx] = user.model_dump()   # replace old with new
            updated = True
            break

    # If not found, append new user
    if not updated:
        users.append(user.model_dump())

    # Save back to file
    with open(file_path, "w") as file:
        json.dump(users, file, indent=4)

    return {
        "message": "User updated successfully" if updated else "User added successfully",
        "user": user
    }



@app.get("/user/{name}")
async def get_user(name: str):
    file_path = os.path.join(os.getcwd(), "users.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="No users found")

    with open(file_path, "r") as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = []

    for user in users:
        if user.get("name") == name:
            return {"user": user}

    raise HTTPException(status_code=404, detail=f"User with name '{name}' not found")


