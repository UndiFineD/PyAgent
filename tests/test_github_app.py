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

client = TestClient(app)


def test_health_endpoint() -> None:
    """GET /health should return 200 with status ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_webhook_receives() -> None:
    """Posting to the /webhook endpoint should return a JSON response indicating the payload was received."""
    resp = client.post("/webhook", json={"action": "opened"})
    assert resp.json()["received"]


def test_webhook_ping_event() -> None:
    """Ping events should be acknowledged with zen message."""
    resp = client.post(
        "/webhook",
        json={"zen": "Keep it logically awesome."},
        headers={"X-GitHub-Event": "ping"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["event"] == "ping"
    assert "Keep it logically awesome" in body["zen"]


def test_webhook_push_event() -> None:
    """Push events should return ref and commit count."""
    payload = {
        "ref": "refs/heads/main",
        "commits": [{"id": "abc"}, {"id": "def"}],
        "repository": {"full_name": "owner/repo"},
    }
    resp = client.post(
        "/webhook",
        json=payload,
        headers={"X-GitHub-Event": "push"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["event"] == "push"
    assert body["commits"] == 2
    assert body["ref"] == "refs/heads/main"


def test_webhook_pull_request_event() -> None:
    """Pull request events return action and PR number."""
    payload = {
        "action": "opened",
        "pull_request": {"number": 42, "title": "My PR"},
        "repository": {"full_name": "owner/repo"},
    }
    resp = client.post(
        "/webhook",
        json=payload,
        headers={"X-GitHub-Event": "pull_request"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["event"] == "pull_request"
    assert body["number"] == 42
    assert body["action"] == "opened"


def test_webhook_issues_event() -> None:
    """Issues events return action and issue number."""
    payload = {
        "action": "labeled",
        "issue": {"number": 7, "title": "Bug report"},
        "repository": {"full_name": "owner/repo"},
    }
    resp = client.post(
        "/webhook",
        json=payload,
        headers={"X-GitHub-Event": "issues"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["event"] == "issues"
    assert body["number"] == 7


def test_webhook_unknown_event() -> None:
    """Unknown events should return received=True without error."""
    resp = client.post(
        "/webhook",
        json={"foo": "bar"},
        headers={"X-GitHub-Event": "star"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["received"] is True
    assert body["event"] == "star"
