# hmac-webhook-verification — Test Plan

_Owner: @5test | Status: DONE_

## Test Strategy

Tests are added to the existing `tests/test_github_app.py` (TDD: written before code).

### Existing tests (must all continue to pass)

| Test | Expected |
|---|---|
| `test_health_endpoint` | 200 |
| `test_webhook_receives` | 200 |
| `test_webhook_ping_event` | 200 |
| `test_webhook_push_event` | 200 |
| `test_webhook_pull_request_event` | 200 |
| `test_webhook_issues_event` | 200 |
| `test_webhook_unknown_event` | 200 |

Note: existing tests send no `GITHUB_WEBHOOK_SECRET` env var, so they operate in
pass-through mode and must remain 200.

### New tests (8)

#### Unit tests for helper function

```python
from src.github_app import verify_github_signature
import hashlib, hmac

def test_verify_signature_helper_true():
    secret = "mysecret"
    body = b'{"action":"opened"}'
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_github_signature(secret, body, sig) is True

def test_verify_signature_helper_false_wrong():
    assert verify_github_signature("secret", b"body", "sha256=deadbeef") is False

def test_verify_signature_helper_false_missing():
    assert verify_github_signature("secret", b"body", None) is False

def test_verify_signature_helper_false_empty_secret():
    assert verify_github_signature("", b"body", "sha256=anything") is False
```

#### Integration tests via HTTP client

```python
import src.github_app as gha
import hashlib, hmac, json
from fastapi.testclient import TestClient

def _sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

def test_webhook_valid_hmac(monkeypatch):
    monkeypatch.setattr(gha, "WEBHOOK_SECRET", "testsecret")
    body = json.dumps({"action": "opened"}).encode()
    client = TestClient(gha.app)
    resp = client.post("/webhook", content=body,
                       headers={"X-GitHub-Event": "ping",
                                "X-Hub-Signature-256": _sign("testsecret", body)})
    assert resp.status_code == 200

def test_webhook_invalid_hmac(monkeypatch):
    monkeypatch.setattr(gha, "WEBHOOK_SECRET", "testsecret")
    body = json.dumps({"action": "opened"}).encode()
    client = TestClient(gha.app)
    resp = client.post("/webhook", content=body,
                       headers={"X-GitHub-Event": "ping",
                                "X-Hub-Signature-256": "sha256=badhash"})
    assert resp.status_code == 401

def test_webhook_missing_signature_header(monkeypatch):
    monkeypatch.setattr(gha, "WEBHOOK_SECRET", "testsecret")
    body = json.dumps({"action": "opened"}).encode()
    client = TestClient(gha.app)
    resp = client.post("/webhook", content=body,
                       headers={"X-GitHub-Event": "ping"})
    assert resp.status_code == 401

def test_webhook_no_secret_configured(monkeypatch):
    monkeypatch.setattr(gha, "WEBHOOK_SECRET", "")
    body = json.dumps({"action": "opened"}).encode()
    client = TestClient(gha.app)
    resp = client.post("/webhook", content=body,
                       headers={"X-GitHub-Event": "ping"})
    assert resp.status_code == 200
```

## Run Command

```powershell
pytest tests/test_github_app.py -v
```

Expected: 15 passed (7 existing + 8 new).
