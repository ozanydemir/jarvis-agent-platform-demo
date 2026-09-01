from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index_renders_agent_console() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Assistant route" in response.text
    assert "Synthetic demo" in response.text


def test_simulation_returns_trace() -> None:
    response = client.post("/simulate", json={"message": "Calculate a synthetic total"})
    assert response.status_code == 200
    assert len(response.json()["trace"]) == 4
