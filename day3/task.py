from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="Sentiment Analysis API")

# Load pretrained Hugging Face sentiment model
sentiment_model = pipeline("sentiment-analysis")


# Define input JSON structure
class TextInput(BaseModel):
    text: str


# POST endpoint to analyze sentiment
@app.post("/analyze")
def analyze_sentiment(input_data: TextInput):
    """
    Accepts JSON with 'text' field, returns sentiment label and score
    """
    text = input_data.text

    try:
        # Hugging Face returns a list of dicts, take first element
        result = sentiment_model(text)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Return label and score as JSON
    return {"label": result["label"], "score": result["score"]}
