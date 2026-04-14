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
"""Tests for SessionManager."""

from unittest.mock import AsyncMock

import pytest

from backend.session_manager import SessionManager


@pytest.mark.asyncio
async def test_connect_returns_session_id():
    manager = SessionManager()
    ws = AsyncMock()
    session_id = await manager.connect(ws)
    assert isinstance(session_id, str)
    assert len(session_id) > 0
    # SessionManager.connect() no longer calls accept() — app.py accepts first.
    ws.accept.assert_not_awaited()


@pytest.mark.asyncio
async def test_disconnect_removes_session():
    manager = SessionManager()
    ws = AsyncMock()
    session_id = await manager.connect(ws)
    manager.disconnect(session_id)
    assert manager.get(session_id) is None


def test_disconnect_nonexistent_session_is_safe():
    manager = SessionManager()
    manager.disconnect("does-not-exist")  # should not raise
