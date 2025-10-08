from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# 1️⃣ Define input data model
class TextRequest(BaseModel):
    text: str

# 2️⃣ Initialize FastAPI
app = FastAPI(title="Sentiment Analysis API")

# 3️⃣ Enable CORS for frontend (any origin allowed for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"]
)

# 4️⃣ Load sentiment analysis pipeline
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True
)

# 5️⃣ Create POST endpoint
@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    result = sentiment_analyzer(request.text)[0]
    return {"label": result["label"], "score": round(result["score"], 4)}
