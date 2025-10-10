from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ===============================
# Step 1: Request & Response Models
# ===============================
class QARequest(BaseModel):
    text: str

class QAResponse(BaseModel):
    answer: str

# ===============================
# Step 2: Load FLAN-T5 Model
# ===============================
MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# ===============================
# Step 3: Answer Generation
# ===============================
def generate_answer(prompt: str) -> str:
    """Generate an answer from input text using FLAN-T5."""
    prompt = prompt.strip()
    if not prompt:
        # Empty prompt should not reach model
        raise ValueError("Input text is empty.")

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ===============================
# Step 4: FastAPI App
# ===============================
app = FastAPI(title="LangChain Q&A API")

@app.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """
    Accepts JSON: {"text": "<your question>"}
    Returns: {"answer": "<model answer>"}
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        answer = generate_answer(text)
        return QAResponse(answer=answer)
    except ValueError as ve:
        # For empty input inside generate_answer (redundant safety)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Any other model/runtime exceptions
        raise HTTPException(status_code=500, detail=str(e))
