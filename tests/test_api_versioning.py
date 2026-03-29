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
"""Tests for API versioning — /v1/api routing and headers.

prj0000066 — api-versioning.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_v1_health_routable():
    """GET /v1/health returns 200 — canonical probe endpoint."""
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_v1_livez_routable():
    """GET /v1/livez returns 200 with alive status."""
    resp = client.get("/v1/livez")
    assert resp.status_code == 200
    assert resp.json() == {"status": "alive"}


def test_v1_readyz_routable():
    """GET /v1/readyz returns 200 with ready status."""
    resp = client.get("/v1/readyz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}


@pytest.mark.parametrize("path", ["/v1/readyz", "/readyz"])
def test_readyz_degraded_when_forced(path: str, monkeypatch: pytest.MonkeyPatch):
    """Readyz endpoints return deterministic degraded payload when forced via env var."""
    monkeypatch.setenv("PYAGENT_READYZ_FORCE_DEGRADED", "1")

    resp = client.get(path)

    assert resp.status_code == 503
    assert resp.json() == {
        "status": "degraded",
        "ready": False,
        "reason": "forced_degraded_env",
    }


def test_v1_agent_log_routable():
    """GET /v1/api/agent-log/0master returns 200 via canonical versioned prefix."""
    resp = client.get("/v1/api/agent-log/0master")
    assert resp.status_code == 200


def test_v1_projects_routable():
    """GET /v1/api/projects returns 200 via canonical versioned prefix."""
    resp = client.get("/v1/api/projects")
    assert resp.status_code == 200


def test_v1_returns_version_header():
    """Versioned /v1/api/ responses include X-API-Version: 1 header."""
    resp = client.get("/v1/api/projects")
    assert resp.headers.get("x-api-version") == "1"


def test_v1_agent_memory_routable():
    """GET /v1/api/agent-doc/0master returns 200 via canonical versioned prefix."""
    resp = client.get("/v1/api/agent-doc/0master")
    assert resp.status_code == 200


def test_unversioned_returns_deprecation_header():
    """Bare /api/ responses include Deprecation: true header."""
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    assert resp.headers.get("deprecation") == "true"
