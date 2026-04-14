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
"""Tests for agent memory persistence endpoints and MemoryStore.

prj0000065 — agent-memory-persistence.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.memory_store import MemoryStore, _memory_path

client = TestClient(app)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_AGENT = "test-agent-memory-prj65"


def _make_store_with_entries(entries: list[dict]) -> MagicMock:
    """Return a mock MemoryStore whose read() returns *entries*."""
    mock = MagicMock(spec=MemoryStore)
    mock.read = AsyncMock(return_value=entries)
    mock.append = AsyncMock(
        side_effect=lambda agent_id, entry: {
            "id": "mock-id",
            "role": entry["role"],
            "content": entry["content"],
            "session_id": entry.get("session_id"),
            "timestamp": "2026-01-01T00:00:00+00:00",
        }
    )
    mock.clear = AsyncMock(return_value=None)
    return mock


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_append_creates_entry():
    """POST returns 201 with id and timestamp."""
    with patch("backend.app.memory_store") as mock_store:
        mock_store.append = AsyncMock(
            return_value={
                "id": "abc-123",
                "role": "user",
                "content": "Hello agent",
                "session_id": None,
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        )
        resp = client.post(
            f"/api/agent-memory/{_AGENT}",
            json={"role": "user", "content": "Hello agent"},
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == "abc-123"
    assert data["role"] == "user"
    assert data["content"] == "Hello agent"
    assert "timestamp" in data


def test_read_returns_entries():
    """GET /api/agent-memory/{agent_id} returns a list of entries."""
    sample = [
        {
            "id": "z",
            "role": "assistant",
            "content": "Hi there",
            "session_id": None,
            "timestamp": "2026-01-01T00:00:01+00:00",
        },
        {"id": "y", "role": "user", "content": "Hello", "session_id": None, "timestamp": "2026-01-01T00:00:00+00:00"},
    ]
    with patch("backend.app.memory_store") as mock_store:
        mock_store.read = AsyncMock(return_value=sample)
        resp = client.get(f"/api/agent-memory/{_AGENT}")
    assert resp.status_code == 200
    entries = resp.json()
    assert isinstance(entries, list)
    assert len(entries) == 2
    assert entries[0]["id"] == "z"


def test_read_limit_param():
    """GET ?limit=1 returns only 1 entry."""
    sample = [
        {
            "id": "z",
            "role": "assistant",
            "content": "Hi there",
            "session_id": None,
            "timestamp": "2026-01-01T00:00:01+00:00",
        },
    ]
    with patch("backend.app.memory_store") as mock_store:
        mock_store.read = AsyncMock(return_value=sample)
        resp = client.get(f"/api/agent-memory/{_AGENT}?limit=1")
    assert resp.status_code == 200
    mock_store.read.assert_awaited_once_with(_AGENT, limit=1)
    assert len(resp.json()) == 1


def test_clear_removes_entries():
    """DELETE returns 204; no body."""
    with patch("backend.app.memory_store") as mock_store:
        mock_store.clear = AsyncMock(return_value=None)
        resp = client.delete(f"/api/agent-memory/{_AGENT}")
    assert resp.status_code == 204
    mock_store.clear.assert_awaited_once_with(_AGENT)


def test_unauthenticated_get_rejected():
    """Endpoints require authentication when credentials are configured."""
    import backend.auth as _auth

    original_dev = _auth.DEV_MODE
    try:
        # Simulate production mode: enable auth enforcement
        _auth.DEV_MODE = False
        _auth.API_KEY = "prod-key"
        resp = client.get(f"/api/agent-memory/{_AGENT}")
        # Should be rejected (401 or 403) when no credentials supplied
        assert resp.status_code in (401, 403)
    finally:
        _auth.DEV_MODE = original_dev
        _auth.API_KEY = ""


def test_invalid_role_missing_content():
    """POST without required 'content' field returns 422."""
    with patch("backend.app.memory_store") as mock_store:
        mock_store.append = AsyncMock(return_value={})
        resp = client.post(
            f"/api/agent-memory/{_AGENT}",
            json={"role": "user"},  # missing content
        )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# MemoryStore unit tests (without HTTP layer)
# ---------------------------------------------------------------------------


def test_memory_path_rejects_traversal():
    """_memory_path raises ValueError for path-traversal attempts."""
    with pytest.raises(ValueError):
        _memory_path("../../../etc/passwd")


def test_memory_path_rejects_slash():
    """_memory_path raises ValueError for agent_id containing '/'."""
    with pytest.raises(ValueError):
        _memory_path("foo/bar")
