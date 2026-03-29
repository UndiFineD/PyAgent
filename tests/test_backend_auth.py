#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for backend.auth — API-key and JWT authentication (prj0000054)."""

from __future__ import annotations

import jwt
import pytest

try:
    from fastapi.testclient import TestClient
except SystemError as exc:
    pytest.skip(f"FastAPI import error: {exc}", allow_module_level=True)

import backend.app as app_mod
import backend.auth as auth_mod

# ---------------------------------------------------------------------------
# Unit tests: verify_api_key
# ---------------------------------------------------------------------------


def test_verify_api_key_match() -> None:
    """verify_api_key should return True for matching values."""
    assert auth_mod.verify_api_key("secret", "secret") is True


def test_verify_api_key_wrong() -> None:
    """verify_api_key should return False for non-matching values."""
    assert auth_mod.verify_api_key("secret", "wrong") is False


def test_verify_api_key_none_provided() -> None:
    """verify_api_key should return False when no key is provided."""
    assert auth_mod.verify_api_key("secret", None) is False


def test_verify_api_key_empty_expected() -> None:
    """verify_api_key should return False when expected key is empty."""
    assert auth_mod.verify_api_key("", "anything") is False


# ---------------------------------------------------------------------------
# Unit tests: verify_jwt
# ---------------------------------------------------------------------------


def test_verify_jwt_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    """verify_jwt should decode a valid token signed with configured secret."""
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    token = jwt.encode({"sub": "user1"}, "test-secret-key-minimum-32-bytes-long!!", algorithm="HS256")
    result = auth_mod.verify_jwt(token)
    assert result is not None
    assert result["sub"] == "user1"


def test_verify_jwt_wrong_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """verify_jwt should reject a token signed with a different secret."""
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    token = jwt.encode({"sub": "user1"}, "other-secret-key-minimum-32-bytes-long!", algorithm="HS256")
    assert auth_mod.verify_jwt(token) is None


def test_verify_jwt_expired(monkeypatch: pytest.MonkeyPatch) -> None:
    """verify_jwt should reject an expired token."""
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    # exp=1 is in the distant past
    token = jwt.encode({"sub": "user1", "exp": 1}, "test-secret-key-minimum-32-bytes-long!!", algorithm="HS256")
    assert auth_mod.verify_jwt(token) is None


def test_verify_jwt_garbage(monkeypatch: pytest.MonkeyPatch) -> None:
    """verify_jwt should reject malformed token text."""
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    assert auth_mod.verify_jwt("notavalidtoken") is None


def test_verify_jwt_none() -> None:
    """verify_jwt should return None when token input is missing."""
    assert auth_mod.verify_jwt(None) is None


# ---------------------------------------------------------------------------
# Integration tests via HTTP TestClient
# ---------------------------------------------------------------------------


def test_health_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """GET /v1/health must return 200 even when auth is fully enforced."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    assert client.get("/v1/health").status_code == 200


def test_livez_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """GET /v1/livez must return 200 even when auth is fully enforced."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    assert client.get("/v1/livez").status_code == 200


def test_readyz_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """GET /v1/readyz must return 200 even when auth is fully enforced."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    assert client.get("/v1/readyz").status_code == 200


def test_rest_no_creds_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
    """Requests without credentials must be rejected when auth is configured."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    assert client.get("/v1/api/projects").status_code == 401


def test_rest_valid_api_key_returns_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid X-API-Key header grants access to protected endpoints."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    resp = client.get("/v1/api/projects", headers={"X-API-Key": "testkey"})
    assert resp.status_code == 200


def test_rest_invalid_api_key_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
    """A wrong API key must be rejected."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    resp = client.get("/v1/api/projects", headers={"X-API-Key": "wrongkey"})
    assert resp.status_code == 401


def test_rest_valid_jwt_returns_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid Bearer token grants access to protected endpoints."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    token = jwt.encode({"sub": "user1"}, "test-secret-key-minimum-32-bytes-long!!", algorithm="HS256")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    resp = client.get("/v1/api/projects", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200


def test_rest_invalid_jwt_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
    """A token signed with the wrong secret must be rejected."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    token = jwt.encode({"sub": "user1"}, "wrong-secret-key-minimum-32-bytes-long!", algorithm="HS256")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    resp = client.get("/v1/api/projects", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_dev_mode_no_creds_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    """In dev mode (no secrets configured), unauthenticated requests pass through."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", True)
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    assert client.get("/v1/api/projects").status_code == 200


def test_both_api_key_and_jwt_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Either credential type is accepted when both are configured."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    token = jwt.encode({"sub": "user1"}, "test-secret-key-minimum-32-bytes-long!!", algorithm="HS256")
    client = TestClient(app_mod.app, raise_server_exceptions=False)
    # API key path
    assert client.get("/v1/api/projects", headers={"X-API-Key": "testkey"}).status_code == 200
    # JWT path
    assert client.get("/v1/api/projects", headers={"Authorization": f"Bearer {token}"}).status_code == 200
