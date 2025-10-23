"""API endpoint tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "YUSEARCH" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_report_validation():
    """Test report generation requires proper fields."""
    # Missing required fields
    response = client.post("/api/reports/generate", json={})
    assert response.status_code == 422  # Validation error

    # Valid request (will fail without API keys, but validates input)
    response = client.post(
        "/api/reports/generate",
        json={
            "prospect_name": "John Doe",
            "company_name": "Acme Corp",
        },
    )
    # Should return 200 and start processing
    assert response.status_code == 200
    assert "report_id" in response.json()


def test_get_nonexistent_report():
    """Test getting a report that doesn't exist."""
    response = client.get("/api/reports/invalid-id")
    assert response.status_code == 404
