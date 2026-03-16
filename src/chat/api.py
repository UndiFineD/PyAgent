#!/usr/bin/env python3
"""API module for PyAgent."""
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

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chat.models import ChatRoom
from MemoryTransactionManager import MemoryTransaction  # ensure atomic updates

try:
    from prometheus_client import Counter
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs

    class _CounterValue:
        """Simple mutable value holder for fallback metrics."""

        def __init__(self) -> None:
            """Initialize value to zero."""
            self._current = 0

        def set(self, value: int) -> None:
            """Set the stored metric value."""
            self._current = value

        def get(self) -> int:
            """Get the stored metric value."""
            return self._current

    class Counter:
        """No-op Prometheus counter fallback."""

        def __init__(self, _name: str, _documentation: str) -> None:
            """Initialize fallback counter."""
            self._value = _CounterValue()

        def inc(self) -> None:
            """Increment counter by one."""
            self._value.set(self._value.get() + 1)


app = FastAPI()

# simple in-memory storage mapping room name to ChatRoom instance
rooms: dict[str, ChatRoom] = {}

# metrics
messages_counter = Counter("chat_messages_total", "Total number of messages posted to chat rooms")


class RoomCreateRequest(BaseModel):
    """Request body for creating a new chat room."""

    name: str
    members: list[str]


class MessageRequest(BaseModel):
    """Request body for posting a message to a chat room."""

    sender: str
    text: str


@app.post("/rooms")
def create_room(request: RoomCreateRequest) -> dict[str, str]:
    """Create a new chat room."""
    # guard against concurrent writers using a memory transaction
    with MemoryTransaction():
        if request.name in rooms:
            raise HTTPException(status_code=400, detail="room already exists")
        rooms[request.name] = ChatRoom(request.name, request.members)
    return {"name": request.name}


@app.post("/rooms/{room_name}/messages")
def post_message(room_name: str, request: MessageRequest) -> dict[str, str]:
    """Post a message to a room."""
    # lookup and mutation must be atomic so we lock with a transaction
    with MemoryTransaction():
        room = rooms.get(room_name)
        if room is None:
            raise HTTPException(status_code=404, detail="room not found")
        room.post(request.sender, request.text)
    # metric tracking (doesn't modify shared memory)
    messages_counter.inc()
    return {"status": "ok"}


@app.get("/rooms/{room_name}/messages")
def get_history(room_name: str) -> list[dict[str, Any]]:
    """Get message history for a room."""
    room = rooms.get(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="room not found")
    return room.history()
