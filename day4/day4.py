# FastAPI & Why Async
# Uses Pydantic library for data validation and serialization.

# Automatically generates API docs (Swagger UI & ReDoc).

# Async allows your API to handle many requests at the same time without waiting for each request to finish.

# Used for :
# Database calls
# External API requests
# File uploads/downloads

import time

# # Synchronous blocking
# def fetch_data():
#     time.sleep(2)  # wait 2 seconds
#     return {"data": "Done"}

# If 10 users call this at the same time, total time = 20 seconds.
# Async version handles all 10 calls in ~2 seconds.

import asyncio

async def fetch_data():
    await asyncio.sleep(2)  # non-blocking
    return {"data": "Done"}


# Run any FastAPI file
# Option A: Run from the file’s folder
# cd path/to/folder
# uvicorn filename:app --reload