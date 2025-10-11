# app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from task import process_pdf, ask_question, db

app = FastAPI(title="LangChain Document Q&A API")

# ------------------------------
# Upload PDF
# ------------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf(file_path)
    return JSONResponse({"message": "PDF uploaded and embeddings stored successfully"})


# ------------------------------
# Ask question
# ------------------------------
@app.post("/ask")
async def ask_endpoint(query: str):
    answer = ask_question(query)
    return JSONResponse({"answer": answer})
