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
"""Red-phase contract tests for backend-managed refresh-session lifecycle."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

import backend.app as app_mod
import backend.auth as auth_mod


def _bootstrap_session(client: TestClient, api_key: str) -> dict[str, Any]:
    """Create a managed auth session via the phase-one bootstrap endpoint."""
    response = client.post("/v1/auth/session", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "Bearer"
    assert payload["subject"] == "service:api_key"
    return payload


@pytest.fixture
def refresh_store_path(tmp_path: Path) -> Path:
    """Provide an isolated refresh-session persistence path for each test."""
    return tmp_path / "refresh_sessions.json"


def test_auth_session_bootstrap_returns_managed_token_pair(
    monkeypatch: pytest.MonkeyPatch,
    refresh_store_path: Path,
) -> None:
    """Valid API-key bootstrap should return managed access/refresh tokens."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "bootstrap-key")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    monkeypatch.setenv("PYAGENT_AUTH_SESSION_STORE_PATH", str(refresh_store_path))

    client = TestClient(app_mod.app, raise_server_exceptions=False)
    response = client.post("/v1/auth/session", headers={"X-API-Key": "bootstrap-key"})

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["access_token"], str)
    assert isinstance(payload["refresh_token"], str)
    assert payload["token_type"] == "Bearer"
    assert payload["expires_in"] > 0
    assert payload["refresh_expires_in"] > 0
    assert isinstance(payload["session_id"], str)
    assert payload["subject"] == "service:api_key"


def test_auth_session_bootstrap_with_invalid_api_key_returns_401(
    monkeypatch: pytest.MonkeyPatch,
    refresh_store_path: Path,
) -> None:
    """Invalid bootstrap credentials must be rejected with unauthorized status."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "bootstrap-key")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    monkeypatch.setenv("PYAGENT_AUTH_SESSION_STORE_PATH", str(refresh_store_path))

    client = TestClient(app_mod.app, raise_server_exceptions=False)
    response = client.post("/v1/auth/session", headers={"X-API-Key": "wrong-key"})

    assert response.status_code == 401


def test_refresh_rotation_rejects_replayed_refresh_token(
    monkeypatch: pytest.MonkeyPatch,
    refresh_store_path: Path,
) -> None:
    """Refresh flow should rotate once and reject replay of the prior token."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "bootstrap-key")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    monkeypatch.setenv("PYAGENT_AUTH_SESSION_STORE_PATH", str(refresh_store_path))

    client = TestClient(app_mod.app, raise_server_exceptions=False)
    bootstrap_payload = _bootstrap_session(client, "bootstrap-key")
    first_refresh_token = bootstrap_payload["refresh_token"]

    first_refresh_response = client.post("/v1/auth/refresh", json={"refresh_token": first_refresh_token})
    assert first_refresh_response.status_code == 200
    rotated_payload = first_refresh_response.json()
    assert rotated_payload["refresh_token"] != first_refresh_token

    replay_response = client.post("/v1/auth/refresh", json={"refresh_token": first_refresh_token})
    assert replay_response.status_code == 401


def test_logout_revokes_refresh_session_family(
    monkeypatch: pytest.MonkeyPatch,
    refresh_store_path: Path,
) -> None:
    """Logout should revoke refresh-session state for subsequent refresh attempts."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "bootstrap-key")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    monkeypatch.setenv("PYAGENT_AUTH_SESSION_STORE_PATH", str(refresh_store_path))

    client = TestClient(app_mod.app, raise_server_exceptions=False)
    bootstrap_payload = _bootstrap_session(client, "bootstrap-key")
    refresh_token = bootstrap_payload["refresh_token"]

    logout_response = client.post("/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_response.status_code == 200
    assert logout_response.json()["status"] == "revoked"

    refresh_after_logout = client.post("/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_after_logout.status_code == 401


def test_refresh_token_is_not_persisted_in_plaintext(
    monkeypatch: pytest.MonkeyPatch,
    refresh_store_path: Path,
) -> None:
    """Persistence contract should not write raw refresh tokens to disk."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "bootstrap-key")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "test-secret-key-minimum-32-bytes-long!!")
    monkeypatch.setenv("PYAGENT_AUTH_SESSION_STORE_PATH", str(refresh_store_path))

    client = TestClient(app_mod.app, raise_server_exceptions=False)
    bootstrap_payload = _bootstrap_session(client, "bootstrap-key")
    refresh_token = bootstrap_payload["refresh_token"]

    assert refresh_store_path.exists()
    persisted = refresh_store_path.read_text(encoding="utf-8")
    assert refresh_token not in persisted
