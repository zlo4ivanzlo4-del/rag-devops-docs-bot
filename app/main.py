from fastapi import FastAPI, HTTPException
from app.models import AskRequest, AskResponse
from app.utils import load_index, ask
import os

app = FastAPI(title="RAG Documentation Assistant")

# Загружаем индекс при старте
chunks_count = load_index()

@app.get("/health")
async def health():
    return {"status": "ok", "chunks_indexed": chunks_count}

@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(req: AskRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = ask(req.question, top_k=req.top_k)
    return result