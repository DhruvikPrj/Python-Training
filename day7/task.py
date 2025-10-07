# text_analysis_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# -----------------------------
# 1️⃣ Define Input Schema
# -----------------------------
class TextInput(BaseModel):
    text: str

# -----------------------------
# 2️⃣ Initialize FastAPI App
# -----------------------------
app = FastAPI(title="Text Analysis API")

# Enable CORS (so frontend apps can call it easily)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 3️⃣ Load Models (Cache on Startup)
# -----------------------------
print("🔄 Loading models... please wait...")

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True
)

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    truncation=True
)

print("✅ Models loaded successfully!")

# -----------------------------
# 4️⃣ Sentiment Endpoint
# -----------------------------
@app.post("/sentiment")
async def analyze_sentiment(input: TextInput):
    """Returns sentiment label and score"""
    result = sentiment_analyzer(input.text)[0]
    return {
        "label": result["label"],
        "score": round(result["score"], 4)
    }

# -----------------------------
# 5️⃣ Summarization Endpoint
# -----------------------------
@app.post("/summary")
async def summarize_text(input: TextInput):
    """Returns a short 2-line summary"""
    summary = summarizer(
        input.text,
        max_length=60,
        min_length=30,
        do_sample=False
    )[0]['summary_text']

    return {"summary": summary}
