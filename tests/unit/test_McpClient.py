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
"""Unit tests for McpClient: JSON-RPC 2.0 stdio transport, correlation, timeouts.

All 8 tests are RED-phase: collection fails with ``ModuleNotFoundError``
because ``src.mcp`` does not yet exist.  That is the expected failure.
"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, call

import pytest

from src.mcp.exceptions import McpCallTimeout, McpProtocolError
from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
from src.mcp.McpServerConfig import McpServerConfig

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(name: str = "test-server", timeout: float = 5.0) -> McpServerConfig:
    """Build a minimal McpServerConfig for McpClient tests.

    Args:
        name: The server's unique name slug.
        timeout: Per-call asyncio.wait_for timeout in seconds.

    Returns:
        A McpServerConfig with safe test defaults.

    """
    return McpServerConfig(
        name=name,
        command=["node", "server.js"],
        env_vars={},
        secret_refs=[],
        allowed_paths=["/workspace"],
        allowed_hosts=[],
        timeout_seconds=timeout,
        restart_policy="on-failure",
        sha256_pin=None,
    )


def _make_process(stdout_responses: list[bytes]) -> MagicMock:
    """Return a mock asyncio.subprocess.Process with pre-programmed stdout lines.

    Args:
        stdout_responses: Ordered list of newline-terminated JSON bytes that
            process.stdout.readline() will return in sequence.  After all
            responses are consumed each subsequent call returns b"" (EOF).

    Returns:
        A MagicMock whose .stdout.readline is an AsyncMock queue and whose
        .stdin.write / .stdin.drain / .stdin.close are also mocked.

    """
    process = MagicMock()
    process.returncode = None
    process.pid = 12345

    responses = list(stdout_responses)

    async def readline() -> bytes:
        """Return the next pre-programmed response line."""
        if responses:
            return responses.pop(0)
        return b""

    process.stdout = MagicMock()
    process.stdout.readline = readline

    process.stdin = MagicMock()
    process.stdin.write = MagicMock()
    process.stdin.drain = AsyncMock()
    process.stdin.close = MagicMock()
    process.stdin.wait_closed = AsyncMock()

    return process


def _jsonrpc_response(req_id: int, result: object) -> bytes:
    """Encode a successful JSON-RPC 2.0 response as newline-terminated bytes.

    Args:
        req_id: The correlation id matching the outgoing request.
        result: The result value to embed in the response.

    Returns:
        A newline-terminated UTF-8 encoded JSON-RPC response bytes object.

    """
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}).encode() + b"\n"


def _jsonrpc_error(req_id: int, code: int = -32603, message: str = "Internal error") -> bytes:
    """Encode a JSON-RPC 2.0 error response as newline-terminated bytes.

    Args:
        req_id: The correlation id matching the outgoing request.
        code: JSON-RPC error code (default: -32603 Internal error).
        message: Human-readable error message.

    Returns:
        A newline-terminated UTF-8 encoded JSON-RPC error bytes object.

    """
    return (
        json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}).encode()
        + b"\n"
    )


_CAPABILITIES_RESPONSE = _jsonrpc_response(
    1,
    {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {"listChanged": False}},
        "serverInfo": {"name": "test-mcp-server", "version": "1.0.0"},
    },
)

_INITIALIZED_NOTIFICATION = (
    json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}).encode() + b"\n"
)

# ---------------------------------------------------------------------------
# TC-CLI-01  initialize sends initialize request to stdin
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_initialize_sends_initialize_request() -> None:
    """initialize() writes a JSON-RPC 'initialize' method message to process stdin.

    Verifies the wire-format contract: the bytes written to stdin contain a
    valid JSON-RPC 2.0 object with method == 'initialize', jsonrpc == '2.0',
    and a non-null id field.
    """
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION])
    config = _make_config()
    client = McpClient(process=process, config=config)

    await client.initialize()

    assert process.stdin.write.called, "No data was written to process stdin"
    all_written: bytes = b"".join(
        c.args[0] for c in process.stdin.write.call_args_list if c.args
    )
    # Find the initialize message among all writes.
    messages = [json.loads(line) for line in all_written.strip().split(b"\n") if line.strip()]
    initialize_msgs = [m for m in messages if m.get("method") == "initialize"]
    assert initialize_msgs, "No JSON-RPC 'initialize' method found in stdin writes"
    msg = initialize_msgs[0]
    assert msg["jsonrpc"] == "2.0", f"Wrong jsonrpc version: {msg['jsonrpc']}"
    assert msg.get("id") is not None, "initialize request must carry a non-null id"


# ---------------------------------------------------------------------------
# TC-CLI-02  initialize parses capabilities response into client.capabilities
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_initialize_parses_capabilities_response() -> None:
    """initialize() populates client.capabilities from the server's capability JSON.

    After a successful handshake the capabilities object should reflect
    'tools': ... as returned by the mock server.
    """
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION])
    config = _make_config()
    client = McpClient(process=process, config=config)

    caps = await client.initialize()

    assert caps is not None, "initialize() must return capabilities (not None)"
    # The tools capability key must be present.
    assert hasattr(caps, "tools") or (isinstance(caps, dict) and "tools" in caps), (
        "capabilities object missing 'tools' entry"
    )


# ---------------------------------------------------------------------------
# TC-CLI-03  list_tools returns 2 McpToolDefinition objects
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_tools_returns_tool_definitions() -> None:
    """list_tools() returns a list of McpToolDefinition instances parsed from server response.

    Mocks the server to return two tool definitions and verifies that both are
    returned as McpToolDefinition objects with correct name attributes.
    """
    tools_response = _jsonrpc_response(
        2,
        {
            "tools": [
                {
                    "name": "read_file",
                    "description": "Read a file",
                    "inputSchema": {"type": "object", "properties": {}},
                },
                {
                    "name": "write_file",
                    "description": "Write a file",
                    "inputSchema": {"type": "object", "properties": {}},
                },
            ]
        },
    )
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION, tools_response])
    config = _make_config()
    client = McpClient(process=process, config=config)
    await client.initialize()

    tools = await client.list_tools()

    assert len(tools) == 2, f"Expected 2 tools, got {len(tools)}"
    for t in tools:
        assert isinstance(t, McpToolDefinition), f"Expected McpToolDefinition, got {type(t)}"
    tool_names = {t.name for t in tools}
    assert tool_names == {"read_file", "write_file"}, f"Unexpected tool names: {tool_names}"


# ---------------------------------------------------------------------------
# TC-CLI-04  call_tool round-trip returns matching content
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_tool_round_trip() -> None:
    """call_tool() returns an McpToolResult whose content matches the mock server response.

    Sends tools/call and verifies the returned McpToolResult.content contains
    the text payload injected by the mock server.
    """
    expected_text = "Issue #42 created successfully"
    tool_result_response = _jsonrpc_response(
        2,
        {"content": [{"type": "text", "text": expected_text}]},
    )
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION, tool_result_response])
    config = _make_config()
    client = McpClient(process=process, config=config)
    await client.initialize()

    result = await client.call_tool("create_issue", {"title": "Bug", "body": "Details"})

    assert isinstance(result, McpToolResult), f"Expected McpToolResult, got {type(result)}"
    assert result.content, "McpToolResult.content must not be empty"
    texts = [item.get("text", "") for item in result.content if isinstance(item, dict)]
    assert expected_text in texts, f"Expected '{expected_text}' in content texts, got {texts}"
    assert result.is_error is False, "Successful call must have is_error=False"


# ---------------------------------------------------------------------------
# TC-CLI-05  call_tool timeout raises McpCallTimeout
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_tool_timeout_raises_McpCallTimeout() -> None:  # noqa: N802
    """call_tool() raises McpCallTimeout when the server never responds within timeout.

    Uses a 0.05-second timeout so the test completes quickly; the mock
    server returns an empty stream (no response) to trigger asyncio.wait_for.
    """
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION])  # no tool response
    config = _make_config(timeout=0.05)  # very short timeout
    client = McpClient(process=process, config=config)
    await client.initialize()

    with pytest.raises(McpCallTimeout):
        await client.call_tool("slow_tool", {})


# ---------------------------------------------------------------------------
# TC-CLI-06  call_tool protocol error raises McpProtocolError
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_tool_protocol_error_raises_McpProtocolError() -> None:  # noqa: N802
    """call_tool() raises McpProtocolError when the server returns a JSON-RPC error object.

    Mocks a server that returns {"error": {...}} in response to tools/call,
    which the client must interpret as McpProtocolError.
    """
    error_response = _jsonrpc_error(2, code=-32600, message="Invalid Request")
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION, error_response])
    config = _make_config()
    client = McpClient(process=process, config=config)
    await client.initialize()

    with pytest.raises(McpProtocolError):
        await client.call_tool("bad_tool", {})


# ---------------------------------------------------------------------------
# TC-CLI-07  close cancels reader task before stdin close
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_close_cancels_reader_task_first() -> None:
    """close() cancels the background reader asyncio.Task before closing stdin.

    Records the order of operations: reader task cancellation must precede
    stdin close to avoid a race where the reader writes to a closed pipe.
    """
    process = _make_process([_CAPABILITIES_RESPONSE, _INITIALIZED_NOTIFICATION])
    config = _make_config()
    client = McpClient(process=process, config=config)
    await client.initialize()

    order: list[str] = []
    original_stdin_close = process.stdin.close

    def recording_stdin_close() -> None:
        """Record stdin close after reader task cancel."""
        order.append("stdin_close")
        original_stdin_close()

    process.stdin.close = recording_stdin_close

    # Patch asyncio.Task.cancel on the client's reader task to record when it is called.
    reader_task = getattr(client, "_reader_task", None)
    assert reader_task is not None, "McpClient must expose _reader_task attribute"

    original_cancel = reader_task.cancel

    def recording_cancel(*args: object) -> bool:
        """Record task cancellation."""
        order.append("task_cancel")
        return original_cancel(*args)

    reader_task.cancel = recording_cancel

    await client.close()

    assert "task_cancel" in order, "Reader task cancel() was never called during close()"
    assert "stdin_close" in order, "process.stdin.close() was never called during close()"
    task_idx = order.index("task_cancel")
    stdin_idx = order.index("stdin_close")
    assert task_idx < stdin_idx, (
        f"Reader task must be cancelled before stdin close; got order {order}"
    )


# ---------------------------------------------------------------------------
# TC-CLI-08  correlation id matches response
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_correlation_id_matches_response() -> None:
    """The request id written to stdin is the same id present in the returned response.

    Makes a single call_tool() and inspects the bytes written to stdin to
    extract the outgoing id, then confirms the mock response carrying that
    same id was successfully matched and resolved.
    """
    # We will capture the written id and build a matching response dynamically.
    written_payloads: list[bytes] = []
    process = _make_process([])  # empty — we'll inject responses dynamically below
    config = _make_config()

    original_write = process.stdin.write

    async def capture_write(data: bytes) -> None:
        """Capture write and queue a correlated response into stdout."""
        written_payloads.append(data)
        original_write(data)

    process.stdin.write = capture_write

    # Pre-load stdout with initialize responses; tool response is injected after write.
    stdout_queue: asyncio.Queue[bytes] = asyncio.Queue()
    await stdout_queue.put(_CAPABILITIES_RESPONSE)
    await stdout_queue.put(_INITIALIZED_NOTIFICATION)

    async def dynamic_readline() -> bytes:
        """Return the next queued stdout line."""
        return await asyncio.wait_for(stdout_queue.get(), timeout=2.0)

    process.stdout.readline = dynamic_readline

    client = McpClient(process=process, config=config)
    await client.initialize()

    # Start call_tool as a background task so we can inject the response mid-call.
    call_task = asyncio.create_task(client.call_tool("ping", {}))
    await asyncio.sleep(0)  # let the request be written

    # Find the call id from the written payload.
    assert written_payloads, "call_tool did not write any bytes to stdin"
    call_payload: bytes = b"".join(written_payloads).strip().split(b"\n")[-1]
    msg = json.loads(call_payload)
    assert "id" in msg, f"Outgoing call_tool message missing 'id': {msg}"
    request_id: int = msg["id"]

    # Enqueue a matching response.
    matched_response = _jsonrpc_response(
        request_id,
        {"content": [{"type": "text", "text": "pong"}]},
    )
    await stdout_queue.put(matched_response)

    result = await call_task
    assert isinstance(result, McpToolResult)
    assert result.content[0]["text"] == "pong", (
        f"Response content mismatch: {result.content}"
    )
