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
"""Contract tests for health, livez, and readyz probe endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_probe_state(monkeypatch: pytest.MonkeyPatch):
    """Reset readiness probe controls between tests for deterministic behavior."""
    monkeypatch.delenv("PYAGENT_READYZ_FORCE_DEGRADED", raising=False)
    monkeypatch.delenv("PYAGENT_READYZ_DEGRADED_REASON", raising=False)
    if hasattr(app.state, "readyz_degraded_reason"):
        delattr(app.state, "readyz_degraded_reason")
    yield
    if hasattr(app.state, "readyz_degraded_reason"):
        delattr(app.state, "readyz_degraded_reason")


def _assert_canonical_alias_parity(
    canonical_path: str,
    alias_path: str,
    expected_status: int,
    expected_payload: dict[str, object],
) -> None:
    """Assert canonical and alias probes return identical status and payload."""
    canonical_response = client.get(canonical_path)
    alias_response = client.get(alias_path)

    assert canonical_response.status_code == expected_status
    assert alias_response.status_code == expected_status
    assert canonical_response.json() == expected_payload
    assert alias_response.json() == expected_payload


def test_health_canonical_alias_parity() -> None:
    """Health canonical and alias endpoints return the same contract payload."""
    _assert_canonical_alias_parity(
        canonical_path="/v1/health",
        alias_path="/health",
        expected_status=200,
        expected_payload={"status": "ok"},
    )


def test_livez_canonical_alias_parity() -> None:
    """Livez canonical and alias endpoints return the same contract payload."""
    _assert_canonical_alias_parity(
        canonical_path="/v1/livez",
        alias_path="/livez",
        expected_status=200,
        expected_payload={"status": "alive"},
    )


def test_readyz_healthy_canonical_alias_parity() -> None:
    """Readyz canonical and alias endpoints return ready payload when healthy."""
    _assert_canonical_alias_parity(
        canonical_path="/v1/readyz",
        alias_path="/readyz",
        expected_status=200,
        expected_payload={"status": "ready"},
    )


def test_readyz_degraded_semantics_from_state_reason() -> None:
    """Readyz returns 503 degraded payload with normalized reason from app state."""
    app.state.readyz_degraded_reason = "Database Timeout"

    _assert_canonical_alias_parity(
        canonical_path="/v1/readyz",
        alias_path="/readyz",
        expected_status=503,
        expected_payload={
            "status": "degraded",
            "ready": False,
            "reason": "database_timeout",
        },
    )


def test_readyz_degraded_semantics_from_forced_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Readyz returns deterministic forced degradation payload from environment."""
    monkeypatch.setenv("PYAGENT_READYZ_FORCE_DEGRADED", "1")
    response_canonical = client.get("/v1/readyz")
    response_alias = client.get("/readyz")

    assert response_canonical.status_code == 503
    assert response_alias.status_code == 503
    assert response_canonical.json() == {
        "status": "degraded",
        "ready": False,
        "reason": "forced_degraded_env",
    }
    assert response_alias.json() == response_canonical.json()
