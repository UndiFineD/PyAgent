#!/usr/bin/env python
"""Test the github_app module."""

import pytest

# FastAPI may fail to import due to pydantic-core version mismatch; skip entire
# module if that happens.
try:
    from fastapi.testclient import TestClient
except SystemError as e:
    pytest.skip(f"Skipping github_app tests due to FastAPI import error: {e}", allow_module_level=True)

from src.github_app import app


def test_webhook_receives() -> None:
    """Posting to the /webhook endpoint should return a JSON response indicating the payload was received."""
    client = TestClient(app)
    resp = client.post("/webhook", json={"action": "opened"})
    assert resp.json()["received"]
