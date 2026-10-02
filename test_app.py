import os

os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("LOCAL_MODEL_ENABLED", "false")

from fastapi.testclient import TestClient

from main import app
from quiz_module import clean_json_block

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_blank():
    response = client.post("/qa", json={"text": "   "})
    assert response.status_code == 422


def test_clean_json_block():
    raw = '```json\n{"questions": []}\n```'
    assert clean_json_block(raw) == '{"questions": []}'


def test_ai_routes_with_mocked_services(monkeypatch):
    monkeypatch.setattr("main.answer_question", lambda text: "mock answer")
    monkeypatch.setattr("main.explain_concept", lambda text: "mock explanation")
    monkeypatch.setattr("main.summarize_text", lambda text: "mock summary")
    monkeypatch.setattr("main.get_learning_recommendations", lambda text, level, weeks: f"{level}-{weeks}")
    monkeypatch.setattr("main.generate_quiz", lambda text: [{
        "question": "Q1", "options": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "Because."
    }, {
        "question": "Q2", "options": ["A", "B", "C", "D"], "correct_answer": "B", "explanation": "Because."
    }, {
        "question": "Q3", "options": ["A", "B", "C", "D"], "correct_answer": "C", "explanation": "Because."
    }])

    assert client.post("/qa", json={"text": "hello"}).json()["result"] == "mock answer"
    assert client.post("/explain", json={"text": "hello"}).json()["result"] == "mock explanation"
    assert client.post("/summarize", json={"text": "hello"}).json()["result"] == "mock summary"
    assert client.post("/learn/recommendations", json={"text": "SQL", "level": "beginner", "weeks": 6}).json()["result"] == "beginner-6"
    assert len(client.post("/quiz", json={"text": "hello"}).json()["questions"]) == 3
