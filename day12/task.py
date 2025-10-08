from transformers import pipeline
from datasets import load_dataset
import random

# Load IMDB dataset
dataset = load_dataset("imdb", split="train")
sample_reviews = [dataset[i]['text'] for i in random.sample(range(len(dataset)), 5)]

# Sentiment analysis pipeline with truncation
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True
)

print("\n5 Random IMDB Reviews with Sentiment:\n")
for review in sample_reviews:
    result = sentiment_analyzer(review)[0]
    print("Review:", review[:100], "...")
    print("Sentiment:", result['label'], "| Score:", round(result['score'], 3))
    print("-" * 50)
