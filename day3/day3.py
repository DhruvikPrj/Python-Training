#Neccessary Dependencies
#pip install fastapi uvicorn transformers torch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Load pretrained sentiment-analysis model
sentiment_model = pipeline("sentiment-analysis")


# Define the JSON structure for input
class TextInput(BaseModel):
    text: str

app = FastAPI(title="Sentiment Analysis API")


@app.post("/analyze")
def analyze_sentiment(input_data: TextInput):
    # Get text from input JSON
    text = input_data.text

    # Run inference
    try:
        result = sentiment_model(text)[0]  # Hugging Face returns a list of dicts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Return JSON with label + score
    return {
        "label": result["label"],
        "score": result["score"]
    }
