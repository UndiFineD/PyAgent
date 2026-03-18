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
"""Tests for WebSocket message handler dispatch."""

import json
from unittest.mock import AsyncMock

import pytest

from backend.session_manager import SessionManager
from backend.ws_handler import handle_message


@pytest.fixture
def ws():
    mock = AsyncMock()
    mock.send_text = AsyncMock()
    return mock


@pytest.fixture
def sessions():
    return SessionManager()


@pytest.mark.asyncio
async def test_init_message_sends_ack(ws, sessions):
    await handle_message(sessions, "s1", ws, {"type": "init", "session_id": "s1"})
    ws.send_text.assert_awaited_once()
    sent = json.loads(ws.send_text.call_args[0][0])
    assert sent["type"] == "initAck"


@pytest.mark.asyncio
async def test_unknown_message_sends_error(ws, sessions):
    await handle_message(sessions, "s1", ws, {"type": "unknownXYZ"})
    ws.send_text.assert_awaited_once()
    sent = json.loads(ws.send_text.call_args[0][0])
    assert sent["type"] == "error"


@pytest.mark.asyncio
async def test_run_task_streams_deltas(ws, sessions):
    await handle_message(
        sessions,
        "s1",
        ws,
        {
            "type": "runTask",
            "task_id": "t1",
            "task": "generateText",
            "payload": {"prompt": "hi"},
        },
    )
    calls = [json.loads(c[0][0]) for c in ws.send_text.await_args_list]
    types = [c["type"] for c in calls]
    assert "taskStarted" in types
    assert "taskDelta" in types
    assert "taskComplete" in types
