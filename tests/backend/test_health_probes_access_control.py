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
"""Access-control and rate-limit behavior tests for probe endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import backend.auth as auth_mod
from backend.app import app

client = TestClient(app, raise_server_exceptions=False)
_PROBE_PATHS = (
    "/v1/health",
    "/health",
    "/v1/livez",
    "/livez",
    "/v1/readyz",
    "/readyz",
)


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


def test_probes_are_unauthenticated_when_auth_is_enforced(monkeypatch: pytest.MonkeyPatch) -> None:
    """Probe paths remain unauthenticated and do not return 401/403."""
    monkeypatch.setattr(auth_mod, "DEV_MODE", False)
    monkeypatch.setattr(auth_mod, "API_KEY", "testkey")
    monkeypatch.setattr(auth_mod, "JWT_SECRET", "")

    protected_response = client.get("/v1/api/projects")
    assert protected_response.status_code == 401

    for path in _PROBE_PATHS:
        response = client.get(path)
        assert response.status_code == 200


def test_probe_paths_are_rate_limit_exempt() -> None:
    """Probe paths never return 429 even under burst traffic from one client."""
    for path in _PROBE_PATHS:
        for _ in range(120):
            response = client.get(path, headers={"X-Forwarded-For": "203.0.113.10"})
            assert response.status_code != 429
