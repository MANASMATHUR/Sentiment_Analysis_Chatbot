from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sentiment Chatbot" in response.text

def test_chat_endpoint_positive():
    response = client.post("/chat", json={"message": "I am happy"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "sentiment" in data
    assert data["sentiment"]["label"] == "Positive"

def test_chat_endpoint_negative():
    response = client.post("/chat", json={"message": "This is bad"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"]["label"] == "Negative"

def test_summary_endpoint():
    # Send a few messages first to populate history
    client.post("/chat", json={"message": "Good"})
    client.post("/chat", json={"message": "Bad"})
    
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "trend" in data
    assert "score" in data
    assert "direction" in data
