# Pydantic is a library FastAPI uses to validate and parse data automatically.

from fastapi import FastAPI,status
from pydantic import BaseModel, Field

app = FastAPI(title="Pydantic Example")

# Define a Pydantic model
class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)  # must be greater than 0
    in_stock: bool = True

# Field(..., min_length=2) → required field with min length 2
# gt=0 → greater than 0
# in_stock → optional, default True


@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "price": item.price, "in_stock": item.in_stock}


# Pass query params after ?
# /items/?max_price=100&category=books


@app.get("/search/")
async def search_items(max_price: float = 100, category: str = "all"):
    return {"max_price": max_price, "category": category}

# GET /search/ → {"max_price": 100, "category": "all"}
# GET /search/?max_price=50 → {"max_price": 50, "category": "all"}
# GET /search/?max_price=50&category=books → {"max_price": 50, "category": "books"}

# Path Parameters
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}


# You can define what your API response should look like using Pydantic:
class ItemResponse(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    # we could add internal fields like ID, timestamp
    return item  # only returns fields defined in ItemResponse

# Benefits:

# Ensures clients only receive fields you want to expose.
# Hides internal fields like passwords, database IDs.
# Automatically validates response data.

# Setting HTTp Status Code :

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Delete logic here
    return  # 204 No Content, no body returned


# Status Code	Meaning

# 200	        OK (default for GET/POST)
# 201	        Created
# 204	        No Content
# 400	        Bad Request
# 404	        Not Found
# 422	        Validation Error (automatic)