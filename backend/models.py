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
"""Pydantic models for WebSocket message schema."""
from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel


# ── Client → Backend ────────────────────────────────────────────────────────

class InitMessage(BaseModel):
    type: Literal["init"]
    session_id: str
    client_info: dict[str, Any] = {}


class RunTaskMessage(BaseModel):
    type: Literal["runTask"]
    task_id: str
    task: str
    payload: dict[str, Any] = {}


class ControlMessage(BaseModel):
    type: Literal["control"]
    task_id: str
    action: Literal["cancel", "pause", "resume"]


class SpeechTranscriptMessage(BaseModel):
    type: Literal["speechTranscript"]
    task_id: Optional[str] = None
    transcript: str
    is_final: bool = True


# WebRTC signaling (client→backend)
class SignalMessage(BaseModel):
    type: Literal["signal"]
    session_id: str
    peer_id: str
    signal_type: Literal["offer", "answer", "ice"]
    payload: dict[str, Any]


# ── Backend → Client ────────────────────────────────────────────────────────

class TaskStartedMessage(BaseModel):
    type: Literal["taskStarted"] = "taskStarted"
    task_id: str
    started_at: str


class TaskDeltaMessage(BaseModel):
    type: Literal["taskDelta"] = "taskDelta"
    task_id: str
    delta: str
    meta: dict[str, Any] = {}


class TaskCompleteMessage(BaseModel):
    type: Literal["taskComplete"] = "taskComplete"
    task_id: str
    result: dict[str, Any]
    status: Literal["success", "error"] = "success"


class TaskErrorMessage(BaseModel):
    type: Literal["taskError"] = "taskError"
    task_id: str
    error: str
    code: str = "UNKNOWN"


class ActionRequestMessage(BaseModel):
    """AI-driven command: backend asks the UI to perform an action."""
    type: Literal["actionRequest"] = "actionRequest"
    action: str
    params: dict[str, Any] = {}
    task_id: Optional[str] = None
