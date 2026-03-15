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
"""Manages active WebSocket sessions."""
from __future__ import annotations

import uuid

from fastapi import WebSocket


class SessionManager:
    """Registry mapping session IDs to their active WebSocket connections."""

    def __init__(self) -> None:
        self._sessions: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def get(self, session_id: str) -> WebSocket | None:
        return self._sessions.get(session_id)

    def all_sessions(self) -> dict[str, WebSocket]:
        return dict(self._sessions)
