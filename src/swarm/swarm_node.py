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
"""SwarmNode — minimal peer with ping/pong message exchange (prj0000022)."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any

from .message_model import Message, validate_message


class SwarmNode:
    """Minimal swarm peer.

    Each node has an ID, can send ping messages, and processes incoming
    messages dispatched by the swarm coordinator.  No actual network I/O
    in T-0; messages are exchanged in-process via asyncio queues.
    """

    def __init__(self, node_id: str | None = None) -> None:
        self.node_id: str = node_id or str(uuid.uuid4())
        self._inbox: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self._running = False

    # ------------------------------------------------------------------
    # Messaging helpers
    # ------------------------------------------------------------------

    def _make_message(self, msg_type: str, destination: str, payload: dict[str, Any]) -> dict[str, Any]:
        import time

        return {
            "id": str(uuid.uuid4()),
            "timestamp": str(time.time()),
            "type": msg_type,
            "priority": "normal",
            "source": self.node_id,
            "destination": destination,
            "payload": payload,
            "checksum": "0",
        }

    async def ping(self, destination: str) -> dict[str, Any]:
        """Build and return a ping message (does not send over the network)."""
        return self._make_message("ping", destination, {"seq": 0})

    async def receive(self, raw: dict[str, Any]) -> dict[str, Any] | None:
        """Process an incoming message and return an optional reply."""
        validate_message(raw)
        msg = Message(**raw)
        if msg.type == "ping":
            return self._make_message("pong", msg.source, {"seq": msg.payload.get("seq", 0)})
        return None

    async def enqueue(self, raw: dict[str, Any]) -> None:
        """Put a raw message dict into the node's inbox."""
        await self._inbox.put(raw)

    async def process_one(self) -> dict[str, Any] | None:
        """Take one message from the inbox and process it."""
        raw = await self._inbox.get()
        return await self.receive(raw)
