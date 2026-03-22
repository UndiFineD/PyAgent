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

"""Minimal swarm peer node with asyncio TCP transport and ping/pong protocol.

Each :class:`SwarmNode` can listen for inbound connections and also
initiate outbound connections to other nodes.  Once connected, peers
exchange JSON-framed messages delimited by newlines.  The built-in
ping/pong exchange lets callers verify connectivity without any
application-layer business logic.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any


class SwarmNode:
    """Minimal asyncio TCP peer node.

    Parameters
    ----------
    node_id:
        Unique identifier for this node.  Defaults to a random UUID string.
    """

    def __init__(self, node_id: str | None = None) -> None:
        self.node_id: str = node_id or str(uuid.uuid4())
        self._server: asyncio.AbstractServer | None = None
        self._host: str = "127.0.0.1"
        self._port: int = 0
        # queue of received messages for inspection in tests / callers
        self.received: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

    # ------------------------------------------------------------------
    # Server lifecycle
    # ------------------------------------------------------------------

    async def start(self, host: str = "127.0.0.1", port: int = 0) -> None:
        """Start the TCP server.  Port 0 lets the OS pick a free port."""
        self._host = host
        self._server = await asyncio.start_server(
            self._handle_inbound, host, port
        )
        # Retrieve the actual bound address (useful when port=0)
        addrs = self._server.sockets
        if addrs:
            self._port = addrs[0].getsockname()[1]

    async def stop(self) -> None:
        """Stop the TCP server and close all connections."""
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    @property
    def address(self) -> tuple[str, int]:
        """Return the (host, port) tuple this node is listening on."""
        return self._host, self._port

    # ------------------------------------------------------------------
    # Outbound connections
    # ------------------------------------------------------------------

    async def connect(self, host: str, port: int) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Open a persistent outbound connection to another node."""
        reader, writer = await asyncio.open_connection(host, port)
        asyncio.ensure_future(self._read_loop(reader))
        return reader, writer

    async def send(self, writer: asyncio.StreamWriter, message: dict[str, Any]) -> None:
        """Serialise *message* as JSON and write it to *writer*."""
        raw = (json.dumps(message) + "\n").encode()
        writer.write(raw)
        await writer.drain()

    # ------------------------------------------------------------------
    # Ping / pong helpers
    # ------------------------------------------------------------------

    async def ping(self, writer: asyncio.StreamWriter) -> None:
        """Send a ping message to the remote peer."""
        await self.send(writer, {"type": "ping", "from": self.node_id})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _handle_inbound(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Called by asyncio when a new inbound connection arrives."""
        try:
            async for msg in self._iter_messages(reader):
                await self._dispatch(msg, writer)
        finally:
            writer.close()

    async def _read_loop(self, reader: asyncio.StreamReader) -> None:
        """Background task that reads messages from an outbound connection."""
        async for msg in self._iter_messages(reader):
            await self.received.put(msg)

    @staticmethod
    async def _iter_messages(reader: asyncio.StreamReader):
        """Yield parsed JSON messages from *reader*, one per newline."""
        while True:
            try:
                line = await reader.readline()
            except (asyncio.IncompleteReadError, ConnectionResetError):
                break
            if not line:
                break
            try:
                yield json.loads(line.decode().strip())
            except json.JSONDecodeError:
                continue

    async def _dispatch(
        self, message: dict[str, Any], writer: asyncio.StreamWriter
    ) -> None:
        """Handle an incoming message and optionally reply."""
        await self.received.put(message)
        if message.get("type") == "ping":
            await self.send(
                writer,
                {"type": "pong", "from": self.node_id, "to": message.get("from")},
            )
