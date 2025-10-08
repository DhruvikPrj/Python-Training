from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hello API", version="1.0")

# Model for POST /echo
class EchoModel(BaseModel):
    message: str

# GET /hello route
@app.get("/hello")
async def hello():
    return {"message": "Hello, FastAPI!"}

# POST /echo route
@app.post("/echo")
async def echo(data: EchoModel):
    return {"echo": data.message}
