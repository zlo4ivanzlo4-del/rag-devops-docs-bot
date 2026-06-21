import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from openai import OpenAI

# Глобальные переменные
model = None
index = None
all_chunks = None
llm_client = None
LLM_MODEL = "deepseek-chat"

def load_index():
    global model, index, all_chunks, llm_client
    project_root = Path(__file__).parent.parent
    model = SentenceTransformer('all-mpnet-base-v2')
    index = faiss.read_index(str(project_root / "faiss_index.bin"))
    with open(project_root / "faiss_meta.pkl", "rb") as f:
        all_chunks = pickle.load(f)
    os.environ["DEEPSEEK_API_KEY"] = "sk-cd17e89639294f6991421c3c7d6ab480"
    llm_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    return len(all_chunks)

def search(question, top_k=6):
    q_emb = model.encode(question, convert_to_numpy=True)
    faiss.normalize_L2(q_emb.reshape(1, -1))
    scores, indices = index.search(q_emb.reshape(1, -1), top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(all_chunks):
            results.append({
                "text": all_chunks[idx]["text"],
                "source": all_chunks[idx]["source"],
                "score": float(score)
            })
    return results

SYSTEM_PROMPT = """Ты — ассистент по технической документации. Отвечай ТОЛЬКО на основании предоставленного контекста.
Если ответа нет в контексте — скажи дословно: «не знаю». В конце ответа укажи источники в квадратных скобках (имя файла)."""

def ask(question, top_k=6):
    hits = search(question, top_k)
    if not hits:
        return {"answer": "не знаю", "sources": [], "hits": []}
    context = "\n\n".join(f"[{i+1}] {h['source']}:\n{h['text']}" for i, h in enumerate(hits))
    try:
        resp = llm_client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0.1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"КОНТЕКСТ:\n{context}\n\nВОПРОС: {question}"}
            ]
        )
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка LLM: {e}"
    return {
        "answer": answer,
        "sources": list(set(h["source"] for h in hits)),
        "hits": hits
    }