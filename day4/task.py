from transformers import pipeline
import time
import json

# 50 example sentences
sentences = [f"This is sentence number {i}" for i in range(1, 51)]

# Load models (first time download happens, then caching is used)
bert_model = pipeline("sentiment-analysis", model="bert-base-uncased")
distilbert_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to measure inference time
def measure_time(model, sentences):
    start_time = time.time()
    results = [model(sentence)[0] for sentence in sentences]
    end_time = time.time()
    total_time = end_time - start_time
    return total_time, results

# Measure BERT inference
bert_time, bert_results = measure_time(bert_model, sentences)
print(f"BERT inference time for 50 sentences: {bert_time:.2f} seconds")

# Measure DistilBERT inference
distil_time, distil_results = measure_time(distilbert_model, sentences)
print(f"DistilBERT inference time for 50 sentences: {distil_time:.2f} seconds")

# Save performance log to JSON
performance_log = {
    "BERT": {"time_seconds": bert_time},
    "DistilBERT": {"time_seconds": distil_time}
}

with open("model_performance.json", "w") as f:
    json.dump(performance_log, f, indent=4)

print("Performance log saved to model_performance.json")
