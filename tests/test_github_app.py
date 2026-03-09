from fastapi.testclient import TestClient

from github_app import app


def test_webhook_receives():
    """Posting to the /webhook endpoint should return a JSON response indicating the payload was received."""
    client = TestClient(app)
    resp = client.post("/webhook", json={"action": "opened"})
    assert resp.json()["received"]
