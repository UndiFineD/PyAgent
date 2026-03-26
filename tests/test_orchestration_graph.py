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
"""Backend tests for the /api/agent-log endpoint powering OrchestrationGraph.

prj0000057 — agent-orchestration-graph
"""
from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)

# Unique test content to avoid cross-test pollution
_TEST_CONTENT = f"test-prj0000057-{uuid.uuid4().hex[:8]}"

# Path to the agent log file written by the PUT endpoint (moved in prj0000074)
_LOG_FILE = Path(__file__).resolve().parents[1] / ".github" / "agents" / "data" / "0master.log.md"


@pytest.fixture(autouse=True)
def _restore_agent_log():
    """Save and restore .github/agents/data/0master.log.md to prevent workspace mutation."""
    existed = _LOG_FILE.exists()
    original = _LOG_FILE.read_text(encoding="utf-8") if existed else None
    yield
    # Restore original state after each test
    if original is not None:
        _LOG_FILE.write_text(original, encoding="utf-8")
    elif _LOG_FILE.exists():
        _LOG_FILE.unlink()


def test_agent_log_endpoint_returns_200() -> None:
    """GET /api/agent-log/0master must return HTTP 200."""
    response = client.get("/api/agent-log/0master")
    assert response.status_code == 200


def test_agent_log_response_has_correct_fields() -> None:
    """GET /api/agent-log/0master response JSON must have a 'content' key."""
    response = client.get("/api/agent-log/0master")
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], str)


def test_agent_log_accepts_put_request() -> None:
    """PUT /api/agent-log/0master with valid body must return HTTP 200."""
    response = client.put(
        "/api/agent-log/0master",
        json={"content": _TEST_CONTENT},
    )
    assert response.status_code == 200


def test_agent_log_put_stores_data() -> None:
    """PUT /api/agent-log/0master response must include status=ok."""
    response = client.put(
        "/api/agent-log/0master",
        json={"content": _TEST_CONTENT},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_agent_log_roundtrip() -> None:
    """PUT then GET /api/agent-log/0master must return the same content."""
    unique_content = f"roundtrip-{uuid.uuid4().hex}"
    put_response = client.put(
        "/api/agent-log/0master",
        json={"content": unique_content},
    )
    assert put_response.status_code == 200

    get_response = client.get("/api/agent-log/0master")
    assert get_response.status_code == 200
    assert get_response.json()["content"] == unique_content
