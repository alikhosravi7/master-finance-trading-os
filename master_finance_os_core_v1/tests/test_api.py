from fastapi.testclient import TestClient
from app.main import app
from app import database

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_research_task():
    with TestClient(app) as client:
        response = client.post("/api/v1/tasks", json={
            "task_type": "research",
            "objective": "Review proposed data source",
            "payload": {}
        })
        assert response.status_code == 200
        assert response.json()["routed_agent"] == "research_agent"
        assert response.json()["approval_required"] is False

def test_sensitive_task_requires_approval():
    with TestClient(app) as client:
        response = client.post("/api/v1/tasks", json={
            "task_type": "trading_analysis",
            "objective": "Analyze gold setup",
            "payload": {}
        })
        assert response.status_code == 200
        assert response.json()["approval_required"] is True
        assert response.json()["status"] == "awaiting_approval"
