#!/usr/bin/env python
"""Test the github_app module."""

import hashlib
import hmac as _hmac
import json as _json

import pytest

# FastAPI may fail to import due to pydantic-core version mismatch; skip entire
# module if that happens.
try:
    from fastapi.testclient import TestClient
except SystemError as e:
    pytest.skip(f"Skipping github_app tests due to FastAPI import error: {e}", allow_module_level=True)

import src.github_app as _gha
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


# ---------------------------------------------------------------------------
# HMAC-SHA256 signature verification tests (prj0000053)
# ---------------------------------------------------------------------------


def _sign(secret: str, body: bytes) -> str:
    """Compute the sha256= signature header value for a given body."""
    digest = _hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


# -- Unit tests for the helper function -------------------------------------


def test_verify_signature_helper_true() -> None:
    """verify_github_signature returns True for a correctly-signed body."""
    secret = "mysecret"
    body = b'{"action":"opened"}'
    sig = _sign(secret, body)
    assert _gha.verify_github_signature(secret, body, sig) is True


def test_verify_signature_helper_false_wrong_hash() -> None:
    """verify_github_signature returns False when the hash is wrong."""
    assert _gha.verify_github_signature("secret", b"body", "sha256=deadbeef") is False


def test_verify_signature_helper_false_missing_header() -> None:
    """verify_github_signature returns False when the header is None."""
    assert _gha.verify_github_signature("secret", b"body", None) is False


def test_verify_signature_helper_false_empty_secret() -> None:
    """verify_github_signature returns False when the secret is empty."""
    assert _gha.verify_github_signature("", b"body", "sha256=anything") is False


# -- Integration tests via HTTP client --------------------------------------


def test_webhook_valid_hmac(monkeypatch: pytest.MonkeyPatch) -> None:
    """A correctly-signed request is accepted (200) when a secret is configured."""
    monkeypatch.setattr(_gha, "WEBHOOK_SECRET", "testsecret")
    body = _json.dumps({"zen": "Keep it logically awesome."}).encode()
    sig = _sign("testsecret", body)
    c = TestClient(_gha.app)
    resp = c.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "ping", "X-Hub-Signature-256": sig},
    )
    assert resp.status_code == 200


def test_webhook_invalid_hmac(monkeypatch: pytest.MonkeyPatch) -> None:
    """A request with the wrong signature is rejected with HTTP 401."""
    monkeypatch.setattr(_gha, "WEBHOOK_SECRET", "testsecret")
    body = _json.dumps({"action": "opened"}).encode()
    c = TestClient(_gha.app)
    resp = c.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "ping", "X-Hub-Signature-256": "sha256=badhash"},
    )
    assert resp.status_code == 401


def test_webhook_missing_signature_header(monkeypatch: pytest.MonkeyPatch) -> None:
    """When a secret is set but no signature header is sent, return HTTP 401."""
    monkeypatch.setattr(_gha, "WEBHOOK_SECRET", "testsecret")
    body = _json.dumps({"action": "opened"}).encode()
    c = TestClient(_gha.app)
    resp = c.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "ping"},
    )
    assert resp.status_code == 401


def test_webhook_no_secret_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """When WEBHOOK_SECRET is empty, requests without a signature pass through (dev mode)."""
    monkeypatch.setattr(_gha, "WEBHOOK_SECRET", "")
    body = _json.dumps({"zen": "Keep it logically awesome."}).encode()
    c = TestClient(_gha.app)
    resp = c.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "ping"},
    )
    assert resp.status_code == 200
