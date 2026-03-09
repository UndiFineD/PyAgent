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

from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter

from chat.models import ChatRoom


app = FastAPI()

# simple in-memory storage mapping room name to ChatRoom instance
rooms: Dict[str, ChatRoom] = {}

# metrics
messages_counter = Counter(
    "chat_messages_total", "Total number of messages posted to chat rooms"
)


class RoomCreateRequest(BaseModel):
    """Request body for creating a new chat room."""
    name: str
    members: list[str]


class MessageRequest(BaseModel):
    """Request body for posting a message to a chat room."""
    sender: str
    text: str


@app.post("/rooms")
def create_room(request: RoomCreateRequest) -> Dict[str, str]:
    """Create a new chat room."""
    if request.name in rooms:
        raise HTTPException(status_code=400, detail="room already exists")
    rooms[request.name] = ChatRoom(request.name, request.members)
    return {"name": request.name}


@app.post("/rooms/{room_name}/messages")
def post_message(room_name: str, request: MessageRequest) -> Dict[str, str]:
    """Post a message to a room."""
    room = rooms.get(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="room not found")
    room.post(request.sender, request.text)
    # metric tracking
    messages_counter.inc()
    return {"status": "ok"}


@app.get("/rooms/{room_name}/messages")
def get_history(room_name: str) -> list[Dict[str, str]]:
    """Get message history for a room."""
    room = rooms.get(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="room not found")
    return room.history()
