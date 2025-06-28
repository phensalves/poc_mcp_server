import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>MCP Server</title>" in response.text

def test_get_supported_languages():
    response = client.get("/supported-languages")
    assert response.status_code == 200
    data = response.json()
    # Python is now a separate service, so it won't be in the main server's list
    assert "python" not in data["languages"]
    assert "ruby" in data["languages"]

def test_get_supported_providers():
    response = client.get("/supported-providers")
    assert response.status_code == 200
    data = response.json()
    assert "mock" in data["providers"]
    assert "openai" in data["providers"]

def test_analyze_python_code_mock_provider():
    response = client.post(
        "/analyze",
        json={"language": "python", "code": "x=1", "provider": "mock"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "python"
    assert "[Mock Suggestion]" in data["analysis"]["refactoring_suggestion"]
    assert "metrics" in data["analysis"]
    assert "issues" in data["analysis"]

def test_analyze_unsupported_language():
    response = client.post(
        "/analyze",
        json={"language": "fortran", "code": "...", "provider": "mock"}
    )
    assert response.status_code == 400