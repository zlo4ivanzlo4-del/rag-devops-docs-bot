import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Тест health
def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["chunks_indexed"] > 0

# 2. Вопрос по FastAPI (должен найти fastapi_body.txt или др.)
def test_ask_fastapi():
    resp = client.post("/ask", json={"question": "How to get data from POST body in FastAPI?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert any("fastapi_body" in s for s in data["sources"])

# 3. Вопрос по scikit-learn
def test_ask_sklearn():
    resp = client.post("/ask", json={"question": "How to preprocess data in sklearn?"})
    assert resp.status_code == 200
    data = resp.json()
    assert any("sklearn_preprocessing" in s for s in data["sources"])

# 4. Вопрос по Docker
def test_ask_docker():
    resp = client.post("/ask", json={"question": "How to run a container with Docker?"})
    assert resp.status_code == 200
    data = resp.json()
    assert any("docker_overview" in s for s in data["sources"])

# 5. Вопрос вне контекста (ожидаем "не знаю")
def test_ask_out_of_scope():
    resp = client.post("/ask", json={"question": "What is the capital of France?"})
    assert resp.status_code == 200
    data = resp.json()
    # Проверяем, что в ответе есть фраза "не знаю" или "no information"
    assert "не знаю" in data["answer"].lower() or "no information" in data["answer"].lower()

# 6. Пустой вопрос → 400
def test_ask_empty():
    resp = client.post("/ask", json={"question": ""})
    assert resp.status_code == 400
    assert "cannot be empty" in resp.json()["detail"].lower()

# 7. Проверка структуры ответа (поля answer, sources, hits)
def test_ask_response_structure():
    resp = client.post("/ask", json={"question": "How to use dependencies in FastAPI?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "sources" in data
    assert "hits" in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["hits"], list)
    if data["hits"]:
        assert "text" in data["hits"][0]
        assert "source" in data["hits"][0]
        assert "score" in data["hits"][0]

# 8. Проверка, что для корректного вопроса sources не пуст
def test_ask_sources_not_empty():
    resp = client.post("/ask", json={"question": "How to create a pipeline in sklearn?"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0
    assert len(data["hits"]) > 0