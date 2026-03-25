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
"""Tests for API versioning — /api/v1/ routing and headers.

prj0000066 — api-versioning.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_v1_health_unversioned_still_works():
    """GET /health (unversioned) returns 200 — load-balancer compatibility."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_v1_agent_log_routable():
    """GET /api/v1/agent-log/0master returns 200 via versioned prefix."""
    resp = client.get("/api/v1/agent-log/0master")
    assert resp.status_code == 200


def test_v1_projects_routable():
    """GET /api/v1/projects returns 200 via versioned prefix."""
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 200


def test_v1_returns_version_header():
    """Versioned /api/v1/ responses include X-API-Version: 1 header."""
    resp = client.get("/api/v1/projects")
    assert resp.headers.get("x-api-version") == "1"


def test_v1_agent_memory_routable():
    """GET /api/v1/agent-doc/0master returns 200 via versioned prefix (memory endpoint not on this branch)."""
    resp = client.get("/api/v1/agent-doc/0master")
    assert resp.status_code == 200


def test_unversioned_returns_deprecation_header():
    """Bare /api/ responses include Deprecation: true header."""
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    assert resp.headers.get("deprecation") == "true"
