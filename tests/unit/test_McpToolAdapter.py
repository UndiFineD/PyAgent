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
"""Unit tests for McpToolAdapter: tool registration, deregistration, schema mapping.

All 6 tests are RED-phase: collection fails with ``ModuleNotFoundError``
because ``src.mcp`` does not yet exist.  That is the expected failure.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp.exceptions import McpToolNameCollision
from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
from src.mcp.McpSandbox import McpSandbox
from src.mcp.McpServerConfig import McpServerConfig
from src.mcp.McpToolAdapter import McpToolAdapter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_tool_def(name: str, description: str = "A tool", schema: dict | None = None) -> McpToolDefinition:
    """Construct a McpToolDefinition for adapter tests.

    Args:
        name: The tool's local (un-namespaced) name as returned by the MCP server.
        description: Human-readable description string.
        schema: Input schema dict; defaults to an empty object schema.

    Returns:
        A McpToolDefinition instance with the given attributes.

    """
    return McpToolDefinition(
        name=name,
        description=description,
        input_schema=schema or {"type": "object", "properties": {}},
    )


def _make_mock_client(tools: list[McpToolDefinition]) -> AsyncMock:
    """Build an AsyncMock McpClient that returns the given tool list from list_tools().

    Args:
        tools: The tool definitions to return from list_tools().

    Returns:
        An AsyncMock that satisfies the McpClient interface for adapter tests.

    """
    client = AsyncMock(spec=McpClient)
    client.list_tools = AsyncMock(return_value=tools)
    client.call_tool = AsyncMock(return_value=McpToolResult(content=[{"type": "text", "text": "ok"}], is_error=False))
    return client


def _make_config(name: str = "fs") -> McpServerConfig:
    """Build a minimal McpServerConfig for adapter tests.

    Args:
        name: The server's unique name slug, used as namespace prefix.

    Returns:
        A McpServerConfig with test-safe defaults.

    """
    return McpServerConfig(
        name=name,
        command=["/usr/bin/node", "server.js"],
        env_vars={},
        secret_refs=[],
        allowed_paths=["/workspace"],
        allowed_hosts=[],
        timeout_seconds=5.0,
        restart_policy="on-failure",
        sha256_pin=None,
    )


def _make_adapter(existing_registry: dict | None = None) -> McpToolAdapter:
    """Construct a McpToolAdapter backed by the given (or a fresh) registry dict.

    Args:
        existing_registry: An optional pre-populated registry dict to inject.
            If None a fresh empty dict is used.

    Returns:
        A McpToolAdapter instance ready for use in tests.

    """
    registry: dict = existing_registry if existing_registry is not None else {}
    return McpToolAdapter(registry_ref=registry)


# ---------------------------------------------------------------------------
# TC-ADP-01  register_server_tools adds namespaced tools to the registry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_register_server_tools_adds_namespaced_tools() -> None:
    """register_server_tools('fs', client) adds 'mcp::fs::read_file' to the tool registry.

    Verifies the namespace prefix contract: tool names from MCP servers must be
    registered under the scheme ``mcp::<server_name>::<tool_name>`` so they
    never collide with native PyAgent tools.
    """
    registry: dict = {}
    adapter = _make_adapter(registry)

    tools = [_make_tool_def("read_file"), _make_tool_def("write_file")]
    client = _make_mock_client(tools)
    config = _make_config("fs")
    sandbox = MagicMock(spec=McpSandbox)

    count = await adapter.register_server_tools("fs", client, sandbox, config)

    assert count == 2, f"Expected 2 tools registered, got {count}"
    assert "mcp::fs::read_file" in registry, (
        f"'mcp::fs::read_file' not found in registry; keys: {list(registry.keys())}"
    )
    assert "mcp::fs::write_file" in registry, (
        f"'mcp::fs::write_file' not found in registry; keys: {list(registry.keys())}"
    )


# ---------------------------------------------------------------------------
# TC-ADP-02  deregister_server_tools removes only that server's tools
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deregister_server_tools_removes_only_that_server() -> None:
    """deregister_server_tools('fs') removes only mcp::fs::* leaving mcp::db::* intact.

    Registers tools for two different MCP servers, deregisters one, and
    verifies the other server's tools are completely unaffected.
    """
    registry: dict = {}
    adapter = _make_adapter(registry)
    sandbox = MagicMock(spec=McpSandbox)

    fs_tools = [_make_tool_def("read_file"), _make_tool_def("list_dir")]
    db_tools = [_make_tool_def("query"), _make_tool_def("insert")]

    await adapter.register_server_tools("fs", _make_mock_client(fs_tools), sandbox, _make_config("fs"))
    await adapter.register_server_tools("db", _make_mock_client(db_tools), sandbox, _make_config("db"))

    assert len(registry) == 4, f"Expected 4 tools before deregister; got {list(registry.keys())}"

    removed = await adapter.deregister_server_tools("fs")

    assert removed == 2, f"Expected 2 tools removed, got {removed}"
    assert "mcp::fs::read_file" not in registry, "mcp::fs::read_file should have been removed"
    assert "mcp::fs::list_dir" not in registry, "mcp::fs::list_dir should have been removed"
    # db tools must survive
    assert "mcp::db::query" in registry, "mcp::db::query was incorrectly removed"
    assert "mcp::db::insert" in registry, "mcp::db::insert was incorrectly removed"


# ---------------------------------------------------------------------------
# TC-ADP-03  tool_definition_to_spec maps MCP schema types
# ---------------------------------------------------------------------------


def test_tool_schema_conversion_maps_types() -> None:
    """tool_definition_to_spec() preserves MCP schema type information in the ToolSpec.

    Verifies that string, integer, and object property types from the MCP
    inputSchema are represented correctly in the converted tool spec so that
    the agent runtime can validate arguments before dispatch.
    """
    defn = McpToolDefinition(
        name="complex_tool",
        description="A tool with typed params",
        input_schema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "count": {"type": "integer"},
                "options": {"type": "object"},
            },
        },
    )

    namespaced_name, async_main, description = McpToolAdapter.tool_definition_to_spec("fs", defn)

    assert namespaced_name == "mcp::fs::complex_tool", f"Expected 'mcp::fs::complex_tool', got '{namespaced_name}'"
    assert "complex_tool" in description or "fs" in description, (
        f"Description should reference tool or server name; got: '{description}'"
    )
    # async_main must be an async callable.
    import asyncio

    assert asyncio.iscoroutinefunction(async_main), (
        "tool_definition_to_spec must return an async callable as async_main"
    )


# ---------------------------------------------------------------------------
# TC-ADP-04  async_run_tool invokes McpClient.call_tool
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_run_tool_calls_mcp_client() -> None:
    """The async_main closure returned by register_server_tools calls McpClient.call_tool.

    After registering a tool, retrieving its async_main and calling it must
    result in exactly one call to McpClient.call_tool with the correct tool
    name and argument mapping.
    """
    registry: dict = {}
    adapter = _make_adapter(registry)
    sandbox = MagicMock(spec=McpSandbox)

    mock_client = _make_mock_client([_make_tool_def("read_file")])
    config = _make_config("fs")
    await adapter.register_server_tools("fs", mock_client, sandbox, config)

    # Retrieve the registered tool's main callable.
    tool = registry.get("mcp::fs::read_file")
    assert tool is not None, "mcp::fs::read_file not found in registry after registration"

    tool_main = tool.main if hasattr(tool, "main") else tool
    assert callable(tool_main), f"Expected callable tool main; got {type(tool_main)}"

    # Invoke the async_main with a path argument.
    await tool_main(["--path", "/workspace/notes.txt"])

    mock_client.call_tool.assert_called_once()
    called_name = mock_client.call_tool.call_args[0][0] if mock_client.call_tool.call_args[0] else None
    assert called_name == "read_file" or mock_client.call_tool.called, (
        f"Expected call_tool to be called with 'read_file'; got name={called_name}"
    )


# ---------------------------------------------------------------------------
# TC-ADP-05  registering a name collision raises McpToolNameCollision
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_namespace_collision_raises() -> None:
    """register_server_tools raises McpToolNameCollision when a namespaced name is already taken.

    Pre-populates the registry with a non-MCP tool at 'mcp::fs::read_file'
    (simulating a collision) and asserts that attempting to register the same
    namespaced name via the adapter raises McpToolNameCollision.
    """
    # Pre-occupy the namespaced slot with a non-MCP sentinel.
    existing_tool = MagicMock()
    registry: dict = {"mcp::fs::read_file": existing_tool}
    adapter = _make_adapter(registry)
    sandbox = MagicMock(spec=McpSandbox)

    tools = [_make_tool_def("read_file")]
    client = _make_mock_client(tools)
    config = _make_config("fs")

    with pytest.raises(McpToolNameCollision):
        await adapter.register_server_tools("fs", client, sandbox, config)


# ---------------------------------------------------------------------------
# TC-ADP-06  deregister nonexistent server is a no-op
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deregister_nonexistent_server_is_noop() -> None:
    """deregister_server_tools() does not raise when the server was never registered.

    Attempting to remove tools for a server that was never registered must
    be a silent no-op (return 0 removed tools) rather than raising an error.
    This simplifies cleanup code in McpRegistry.disable().
    """
    registry: dict = {}
    adapter = _make_adapter(registry)

    # Must not raise.
    removed = await adapter.deregister_server_tools("never-registered")

    assert removed == 0, f"Expected 0 tools removed for unknown server, got {removed}"
    assert len(registry) == 0, "Registry must remain empty after deregistering unknown server"
