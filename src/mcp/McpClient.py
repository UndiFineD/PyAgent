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
"""JSON-RPC 2.0 stdio client for MCP servers.

This module provides the wire-level communication layer between PyAgent and
an external MCP server subprocess.  See ``src/mcp/McpSandbox.py`` for the
subprocess lifecycle and ``src/mcp/McpToolAdapter.py`` for tool registration.

Classes:
    McpToolDefinition: Immutable description of one tool exposed by a server.
    McpToolResult:     The response payload returned by a successful tool call.
    McpClient:         Async JSON-RPC 2.0 client bound to a subprocess's stdio.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Optional

from src.mcp.exceptions import McpCallTimeout, McpProtocolError, McpServerCrashed
from src.mcp.McpServerConfig import McpServerConfig

__all__ = ["McpClient", "McpToolDefinition", "McpToolResult"]


@dataclass(frozen=True)
class McpToolDefinition:
    """Immutable description of a tool exposed by an MCP server.

    Attributes:
        name: The tool's local (un-namespaced) name as returned by the server.
        description: Human-readable description string.
        input_schema: JSON Schema dict describing the tool's input parameters.

    """

    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class McpToolResult:
    """Result payload returned by a successful MCP tool call.

    Attributes:
        content: List of content blocks (each is a dict with a ``"type"`` key).
        is_error: ``True`` when the server returned an error result block.

    """

    content: list[dict[str, Any]]
    is_error: bool = False


class McpClient:
    """Async JSON-RPC 2.0 client for an MCP server subprocess.

    One :class:`McpClient` instance is bound to a single subprocess.  A
    background reader task dispatches incoming responses to the correct
    outstanding :class:`asyncio.Future` via integer message correlation IDs.

    The client supports ≥10 concurrent outstanding requests without any
    internal serialisation lock.

    Args:
        process: An :class:`asyncio.subprocess.Process` whose stdin / stdout
            are connected to the MCP server.
        timeout_seconds: Default per-call timeout forwarded as
            ``asyncio.wait_for`` deadline.

    """

    def __init__(
        self,
        process: asyncio.subprocess.Process,
        config: McpServerConfig,
    ) -> None:
        """Initialise the client with a running subprocess.

        Args:
            process: The asyncio subprocess whose stdio streams are used.
            config: Server configuration; ``config.timeout_seconds`` is used
                as the per-call ``asyncio.wait_for`` deadline.

        """
        self._process = process
        self._config = config
        self._timeout: float = config.timeout_seconds
        self._pending: dict[int, asyncio.Future[Any]] = {}
        self._response_cache: dict[int, dict[str, Any]] = {}
        self._next_id: int = 1
        self._reader_task: Optional[asyncio.Task[None]] = None

    async def initialize(self) -> dict[str, Any]:
        """Send the JSON-RPC ``initialize`` handshake and start the reader task.

        Must be called once before any :meth:`call_tool` invocation.

        Returns:
            The ``"capabilities"`` dict received from the server.

        Raises:
            McpServerCrashed: If the server process exits before responding.
            McpProtocolError: If the server's initialize response is malformed.
            McpCallTimeout: If the server does not respond within the timeout.

        """
        self._reader_task = asyncio.create_task(self._read_loop(), name="mcp-reader")
        request_id = self._next_id
        self._next_id += 1
        fut: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = fut
        payload = (
            '{"jsonrpc":"2.0","id":'
            + str(request_id)
            + ',"method":"initialize","params":{"protocolVersion":"2024-11-05",'
            '"capabilities":{},"clientInfo":{"name":"PyAgent","version":"1.0"}}}\n'
        )
        assert self._process.stdin is not None  # noqa: S101
        write_result = self._process.stdin.write(payload.encode())
        if asyncio.iscoroutine(write_result) or asyncio.isfuture(write_result):
            await write_result
        await self._process.stdin.drain()
        try:
            result = await asyncio.wait_for(fut, timeout=self._timeout)
        except asyncio.TimeoutError as exc:
            raise McpCallTimeout("initialize timed out") from exc
        return result.get("capabilities", {})

    async def list_tools(self) -> list[McpToolDefinition]:
        """Request the server's tool manifest via JSON-RPC ``tools/list``.

        Returns:
            Ordered list of :class:`McpToolDefinition` objects.

        Raises:
            McpCallTimeout: If the response exceeds ``timeout_seconds``.
            McpProtocolError: If the response cannot be parsed.

        """
        response = await self._rpc_call("tools/list", {})
        tools_raw = response.get("tools", [])
        result = []
        for item in tools_raw:
            result.append(
                McpToolDefinition(
                    name=item["name"],
                    description=item.get("description", ""),
                    input_schema=item.get("inputSchema", {}),
                )
            )
        return result

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> McpToolResult:
        """Invoke a tool by name and return the result.

        Args:
            tool_name: The un-namespaced tool name as returned by
                :meth:`list_tools`.
            arguments: Keyword arguments forwarded to the server's tool handler.

        Returns:
            A :class:`McpToolResult` with the server's response payload.

        Raises:
            McpCallTimeout: If the response exceeds ``timeout_seconds``.
            McpProtocolError: If the response cannot be parsed.
            McpServerCrashed: If the server process exits during the call.

        """
        response = await self._rpc_call("tools/call", {"name": tool_name, "arguments": arguments})
        content = response.get("content", [])
        is_error = bool(response.get("isError", False))
        return McpToolResult(content=content, is_error=is_error)

    async def ping(self) -> bool:
        """Send a JSON-RPC ``ping`` and return ``True`` on success.

        Returns:
            ``True`` if the server responds within the timeout.

        Raises:
            McpCallTimeout: If the ping times out.

        """
        await self._rpc_call("ping", {})
        return True

    async def close(self) -> None:
        """Cancel the background reader and close the stdin stream.

        Cancels the reader task first to avoid writing to a closed pipe,
        then closes stdin.  Safe to call multiple times.
        """
        if self._reader_task is not None:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except (asyncio.CancelledError, Exception):  # noqa: S110, BLE001
                pass  # Task may have ended normally, been cancelled, or raised; all are safe.
        if self._process.stdin:
            self._process.stdin.close()
            await self._process.stdin.wait_closed()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _rpc_call(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Send a JSON-RPC request and await its response future.

        Args:
            method: The JSON-RPC method name.
            params: The method parameters dict.

        Returns:
            The ``"result"`` payload from the response.

        Raises:
            McpCallTimeout: If the response is not received within the timeout.
            McpProtocolError: If the response is malformed.
            McpServerCrashed: If the server process exits while waiting.

        """
        import json

        request_id = self._next_id
        self._next_id += 1
        fut: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = fut

        payload = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}) + "\n"
        assert self._process.stdin is not None  # noqa: S101
        write_result = self._process.stdin.write(payload.encode())
        if asyncio.iscoroutine(write_result) or asyncio.isfuture(write_result):
            await write_result
        await self._process.stdin.drain()

        # Check if the response was pre-delivered by the reader before we registered
        # the future (can happen when readline returns immediately with no suspension).
        cached = self._response_cache.pop(request_id, None)
        if cached is not None:
            self._pending.pop(request_id, None)
            if "error" in cached:
                raise McpProtocolError(str(cached["error"]))
            return cached.get("result", {})  # type: ignore[return-value]

        try:
            result = await asyncio.wait_for(asyncio.shield(fut), timeout=self._timeout)
        except asyncio.TimeoutError as exc:
            self._pending.pop(request_id, None)
            raise McpCallTimeout(f"'{method}' timed out after {self._timeout}s") from exc

        return result  # type: ignore[return-value]

    async def _read_loop(self) -> None:
        """Background task: read newline-delimited JSON from server stdout.

        Resolves pending futures by correlating the ``"id"`` field.
        Terminates when the stdout stream reaches EOF.
        """
        import json

        assert self._process.stdout is not None  # noqa: S101
        while True:
            try:
                line = await self._process.stdout.readline()
            except Exception:  # noqa: BLE001
                break
            if not line:
                # EOF — server has closed stdout
                for fut in self._pending.values():
                    if not fut.done():
                        fut.set_exception(McpServerCrashed("server stdout closed unexpectedly"))
                self._pending.clear()
                break
            try:
                msg = json.loads(line.decode())
            except json.JSONDecodeError as exc:
                # Discard malformed lines; don't crash the reader.
                _ = exc
                continue
            msg_id = msg.get("id")
            if msg_id is None:
                continue  # notification — ignore for now
            fut = self._pending.pop(msg_id, None)
            if fut is None or fut.done():
                # Response arrived before caller registered a future; cache it.
                self._response_cache[msg_id] = msg
                continue
            if "error" in msg:
                fut.set_exception(McpProtocolError(str(msg["error"])))
            else:
                fut.set_result(msg.get("result", {}))
