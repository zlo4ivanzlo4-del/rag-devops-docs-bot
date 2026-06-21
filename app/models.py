from pydantic import BaseModel
from typing import List

class AskRequest(BaseModel):
    question: str
    top_k: int = 6

class Hit(BaseModel):
    text: str
    source: str
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    hits: List[Hit]