from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Store API", version="1.0")

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
async def root():
    """Returns a greeting message"""
    return {"message": "Hello, FastAPI!"}

@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    return {"item_name": item.name, "item_price": item.price}
