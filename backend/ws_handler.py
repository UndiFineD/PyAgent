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
"""Dispatches WebSocket messages to the appropriate handler."""
from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
from typing import Any

from fastapi import WebSocket

from .models import (
    TaskCompleteMessage,
    TaskDeltaMessage,
    TaskStartedMessage,
)
from .session_manager import SessionManager

logger = logging.getLogger(__name__)


def _build_task_text(data: dict[str, Any]) -> str:
    """Build deterministic task output text from request content.

    Args:
        data: Incoming runTask payload from the websocket client.

    Returns:
        A non-empty text string derived from task fields.

    """
    payload = data.get("payload")
    prompt = ""
    if isinstance(payload, dict):
        raw_prompt = payload.get("prompt", "")
        if isinstance(raw_prompt, str):
            prompt = raw_prompt.strip()

    if prompt:
        return prompt

    task_name = data.get("task")
    if isinstance(task_name, str) and task_name.strip():
        return f"Task '{task_name.strip()}' accepted"

    return "Task accepted"


def _iter_text_chunks(text: str) -> list[str]:
    """Split text into stream-friendly chunks while preserving spacing.

    Args:
        text: Source text to stream over the websocket.

    Returns:
        A list of chunk strings suitable for task delta events.

    """
    chunks = re.findall(r"\S+\s*", text)
    return chunks if chunks else [text]


async def handle_message(
    sessions: SessionManager,
    session_id: str,
    websocket: WebSocket,
    data: dict[str, Any],
) -> None:
    msg_type = data.get("type")
    if msg_type == "init":
        await websocket.send_text(json.dumps({
            "type": "initAck",
            "session_id": session_id,
            "server_version": "0.1.0",
        }))
    elif msg_type == "runTask":
        await _handle_run_task(websocket, data)
    elif msg_type == "control":
        await _handle_control(websocket, data)
    elif msg_type == "speechTranscript":
        await _handle_speech(websocket, data)
    elif msg_type == "signal":
        await _handle_signal(sessions, session_id, data)
    else:
        await websocket.send_text(json.dumps({
            "type": "error",
            "error": f"Unknown message type: {msg_type}",
        }))


async def _handle_run_task(websocket: WebSocket, data: dict[str, Any]) -> None:
    """Process a runTask message and stream result deltas.

    Args:
        websocket: Active websocket connection for the session.
        data: Parsed client message payload.

    """
    task_id = data.get("task_id", "unknown")
    now = datetime.now(timezone.utc).isoformat()

    # Acknowledge start
    await websocket.send_text(TaskStartedMessage(
        task_id=task_id, started_at=now
    ).model_dump_json())

    task_text = _build_task_text(data)
    chunks = _iter_text_chunks(task_text)
    for token in chunks:
        await asyncio.sleep(0.05)
        await websocket.send_text(TaskDeltaMessage(
            task_id=task_id, delta=token
        ).model_dump_json())

    # Complete
    await websocket.send_text(TaskCompleteMessage(
        task_id=task_id,
        result={"text": task_text},
        status="success",
    ).model_dump_json())


async def _handle_control(websocket: WebSocket, data: dict[str, Any]) -> None:
    task_id = data.get("task_id", "unknown")
    action = data.get("action", "cancel")
    logger.info("Control action '%s' for task %s", action, task_id)
    await websocket.send_text(json.dumps({
        "type": "controlAck", "task_id": task_id, "action": action,
    }))


async def _handle_speech(websocket: WebSocket, data: dict[str, Any]) -> None:
    transcript = data.get("transcript", "")
    logger.info("Speech transcript received: %s", transcript[:80])
    # Forward to AI as a runTask (route transcript as a prompt)
    await _handle_run_task(websocket, {
        "task_id": data.get("task_id", "speech"),
        "task": "generateText",
        "payload": {"prompt": transcript},
    })


async def _handle_signal(
    sessions: SessionManager,
    sender_id: str,
    data: dict[str, Any],
) -> None:
    """Relay WebRTC signaling messages between peers."""
    peer_id = data.get("peer_id")
    peer_ws = sessions.get(peer_id) if peer_id else None
    if peer_ws:
        relay = {**data, "from_peer_id": sender_id}
        await peer_ws.send_text(json.dumps(relay))
    else:
        logger.warning("Signal relay: peer %s not found", peer_id)
