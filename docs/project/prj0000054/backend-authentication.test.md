# backend-authentication — Test Plan

_Owner: @5test | Status: DONE_

## Strategy

TDD approach: test file written first, then implementation.
`tests/test_backend_auth.py` uses `pytest` + `monkeypatch` + FastAPI `TestClient`.

## Test Cases

### Unit tests for auth helpers

```python
import hashlib, hmac as _hmac, time
import pytest
import backend.auth as auth_mod
import jwt

def test_verify_api_key_match():
    assert auth_mod.verify_api_key("secret", "secret") is True

def test_verify_api_key_wrong():
    assert auth_mod.verify_api_key("secret", "wrong") is False

def test_verify_api_key_none_provided():
    assert auth_mod.verify_api_key("secret", None) is False

def test_verify_api_key_empty_expected():
    assert auth_mod.verify_api_key("", "anything") is False

def test_verify_jwt_valid(monkeypatch):
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "testsecret")
    token = jwt.encode({"sub": "user1"}, "testsecret", algorithm="HS256")
    result = auth_mod.verify_jwt(token)
    assert result is not None
    assert result["sub"] == "user1"

def test_verify_jwt_wrong_secret(monkeypatch):
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "testsecret")
    token = jwt.encode({"sub": "user1"}, "othersecret", algorithm="HS256")
    assert auth_mod.verify_jwt(token) is None

def test_verify_jwt_expired(monkeypatch):
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "testsecret")
    token = jwt.encode({"sub": "user1", "exp": 1}, "testsecret", algorithm="HS256")
    assert auth_mod.verify_jwt(token) is None

def test_verify_jwt_garbage():
    assert auth_mod.verify_jwt("notavalidtoken") is None

def test_verify_jwt_none():
    assert auth_mod.verify_jwt(None) is None
```

### Integration tests via HTTP TestClient

```python
from fastapi.testclient import TestClient
import backend.app as app_mod

def test_health_no_auth(monkeypatch):
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    client = TestClient(app_mod.app)
    assert client.get("/health").status_code == 200

def test_rest_no_creds_returns_401(monkeypatch):
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app)
    assert client.get("/api/projects").status_code == 401

def test_rest_valid_api_key(monkeypatch):
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app)
    resp = client.get("/api/projects", headers={"X-API-Key": "testkey"})
    assert resp.status_code == 200

def test_rest_valid_jwt(monkeypatch):
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "testsecret")
    token = jwt.encode({"sub": "user1"}, "testsecret", algorithm="HS256")
    client = TestClient(app_mod.app)
    resp = client.get("/api/projects", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_dev_mode_no_auth_passes(monkeypatch):
    monkeypatch.setattr(auth_mod, "DEV_MODE", True)
    client = TestClient(app_mod.app)
    assert client.get("/api/projects").status_code == 200
```

## Run Command

```powershell
pytest tests/test_backend_auth.py -v
```

Expected: ≥ 14 passed.
