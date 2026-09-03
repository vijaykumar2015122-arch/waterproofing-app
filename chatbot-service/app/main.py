from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Waterproofing Chatbot Service")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip().lower()

    if message in {"hello", "hi", "hey"}:
        return {
            "reply": "Hi! I'm here to help you!! Thanks for reaching out to me!"
        }

    return {
        "reply": "Hi! I'm here to help you!! Thanks for reaching out to me!"
    }

