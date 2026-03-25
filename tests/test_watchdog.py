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

import asyncio

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.watchdog import AgentWatchdog


# ---------------------------------------------------------------------------
# Test 1 — Successful task returns {"status": "ok"}
# ---------------------------------------------------------------------------

def test_run_success():
    async def good_coro():
        return "done"

    wd = AgentWatchdog(timeout_s=5.0, max_retries=3)
    result = asyncio.run(wd.run("agent1", good_coro()))
    assert result["status"] == "ok"
    assert result["agent_id"] == "agent1"
    assert result["result"] == "done"


# ---------------------------------------------------------------------------
# Test 2 — Timeout increments retry count
# ---------------------------------------------------------------------------

def test_run_timeout_increments_retry():
    async def slow_coro():
        await asyncio.sleep(10)

    wd = AgentWatchdog(timeout_s=0.01, max_retries=5)
    result = asyncio.run(wd.run("agent2", slow_coro()))
    assert result["status"] == "timeout"
    assert result["retries"] == 1
    assert wd._retry_counts["agent2"] == 1


# ---------------------------------------------------------------------------
# Test 3 — Exhausting retries sends task to DLQ
# ---------------------------------------------------------------------------

def test_run_dead_letter_after_retries():
    async def slow_coro():
        await asyncio.sleep(10)

    # max_retries=2 means retries<2 → timeout, retries>=2 → DLQ
    wd = AgentWatchdog(timeout_s=0.01, max_retries=2)

    async def drive():
        result = None
        for _ in range(3):
            result = await wd.run("agent3", slow_coro())
            if result["status"] == "dead_letter":
                break
        return result

    result = asyncio.run(drive())
    assert result["status"] == "dead_letter"
    assert len(wd.dead_letter_queue) == 1
    assert wd.dead_letter_queue[0]["agent_id"] == "agent3"


# ---------------------------------------------------------------------------
# Test 4 — status() dict has required keys
# ---------------------------------------------------------------------------

def test_status_returns_correct_shape():
    wd = AgentWatchdog(timeout_s=15.0, max_retries=2)
    s = wd.status()
    assert "timeout_s" in s
    assert "max_retries" in s
    assert "dlq_size" in s
    assert "retry_counts" in s
    assert s["timeout_s"] == 15.0
    assert s["max_retries"] == 2


# ---------------------------------------------------------------------------
# Test 5 — DLQ entry has agent_id and timestamp
# ---------------------------------------------------------------------------

def test_dlq_contains_correct_entry():
    async def slow_coro():
        await asyncio.sleep(10)

    wd = AgentWatchdog(timeout_s=0.01, max_retries=1)

    async def drive():
        for _ in range(3):
            r = await wd.run("agent5", slow_coro())
            if r["status"] == "dead_letter":
                break

    asyncio.run(drive())
    assert len(wd.dead_letter_queue) >= 1
    entry = wd.dead_letter_queue[0]
    assert entry["agent_id"] == "agent5"
    assert "timestamp" in entry
    assert isinstance(entry["timestamp"], float)


# ---------------------------------------------------------------------------
# Test 6 — GET /api/watchdog/status endpoint
# ---------------------------------------------------------------------------

def test_watchdog_status_endpoint():
    client = TestClient(app)
    response = client.get("/api/watchdog/status")
    assert response.status_code == 200
    data = response.json()
    assert "timeout_s" in data
    assert "max_retries" in data
    assert "dlq_size" in data
    assert "retry_counts" in data
