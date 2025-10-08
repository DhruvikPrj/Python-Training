from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Pydantic + Params Example")

# Pydantic Models
class Item(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    in_stock: bool = True

class ItemResponse(BaseModel):
    name: str
    price: float

# GET with Query Params
@app.get("/search/")
async def search_items(max_price: float = 100, category: str = "all"):
    return {"max_price": max_price, "category": category}

# GET with Path Param
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# POST with Pydantic + Response Model + Status Code
@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
