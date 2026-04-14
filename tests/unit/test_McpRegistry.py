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
"""Unit tests for McpRegistry lifecycle management.

All 9 tests are RED-phase: collection fails with ``ModuleNotFoundError``
because ``src.mcp`` does not yet exist.  That is the expected failure.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from src.mcp.exceptions import McpServerAlreadyEnabled, McpServerNotEnabled, McpServerNotFound
from src.mcp.McpRegistry import McpRegistry
from src.mcp.McpServerConfig import McpServerConfig

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_SERVER_DICT = {
    "name": "test-server",
    "command": ["node", "server.js"],
    "env_vars": {},
    "secret_refs": [],
    "allowed_paths": ["/workspace"],
    "allowed_hosts": [],
    "timeout_seconds": 5.0,
    "restart_policy": "on-failure",
    "sha256_pin": None,
}


@pytest.fixture()
def registry() -> McpRegistry:
    """Return a fresh, empty McpRegistry instance."""
    return McpRegistry()


@pytest.fixture()
def loaded_registry() -> McpRegistry:
    """McpRegistry pre-loaded with one server config via yaml mock."""
    reg = McpRegistry()
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        import asyncio as _asyncio

        _asyncio.get_event_loop().run_until_complete(reg.load_config("mcp_servers.yml"))
    return reg


# ---------------------------------------------------------------------------
# TC-REG-01  load_config populates servers
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_load_config_populates_servers(registry: McpRegistry) -> None:
    """load_config with a mocked YAML fixture populates list_servers with expected configs.

    Verifies that McpRegistry correctly parses the YAML dict produced by
    PyYAML and constructs McpServerConfig entries that are retrievable via
    list_servers().
    """
    two_servers = [_SERVER_DICT, {**_SERVER_DICT, "name": "other-server"}]
    with patch("yaml.safe_load", return_value=two_servers), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    servers = registry.list_servers()
    assert len(servers) == 2, f"Expected 2 servers, got {len(servers)}"
    names = {s.name for s in servers}
    assert "test-server" in names
    assert "other-server" in names
    for s in servers:
        assert isinstance(s, McpServerConfig), f"Expected McpServerConfig, got {type(s)}"


# ---------------------------------------------------------------------------
# TC-REG-02  enable calls McpSandbox.spawn + McpClient.initialize
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_enable_starts_sandbox_and_client(registry: McpRegistry) -> None:
    """enable() spawns a sandbox process and runs the McpClient initialize handshake.

    Both McpSandbox.spawn and McpClient.initialize must be called exactly once
    for a successful enable().
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    mock_process = MagicMock()
    mock_client = AsyncMock()
    mock_client.list_tools = AsyncMock(return_value=[])

    with (
        patch("src.mcp.McpRegistry.McpSandbox") as mock_sandbox_cls,
        patch("src.mcp.McpRegistry.McpClient") as mock_client_cls,
        patch("src.mcp.McpRegistry.McpToolAdapter"),
    ):
        mock_sandbox_instance = mock_sandbox_cls.return_value
        mock_sandbox_instance.spawn = AsyncMock(return_value=mock_process)

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.initialize = AsyncMock()
        mock_client_instance.list_tools = AsyncMock(return_value=[])

        await registry.enable("test-server")

    mock_sandbox_instance.spawn.assert_called_once()
    mock_client_instance.initialize.assert_called_once()


# ---------------------------------------------------------------------------
# TC-REG-03  disable drains in-flight before terminate
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_disable_drains_inflight_before_terminate(registry: McpRegistry) -> None:
    """disable() waits for in-flight calls to finish before calling McpSandbox.terminate().

    Sets the internal in-flight counter to 1, starts disable() as a background
    task, asserts terminate was NOT called while draining, then clears the
    in-flight counter and verifies terminate IS called afterward.
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    mock_process = MagicMock()
    terminate_order: list[str] = []

    async def ordered_terminate(_process: object) -> None:
        """Record when terminate is called relative to drain."""
        terminate_order.append("terminate")

    mock_sandbox = MagicMock()
    mock_sandbox.terminate = ordered_terminate

    # Inject running server state directly so we can manipulate in-flight counter.
    registry._processes = {"test-server": mock_process}  # type: ignore[attr-defined]
    registry._sandboxes = {"test-server": mock_sandbox}  # type: ignore[attr-defined]

    from src.mcp.McpRegistry import McpServerStatus  # noqa: PLC0415

    registry._status = {"test-server": McpServerStatus.RUNNING}  # type: ignore[attr-defined]

    drain_event = asyncio.Event()
    registry._drain_events = {"test-server": drain_event}  # type: ignore[attr-defined]
    registry._in_flight_counts = {"test-server": 1}  # type: ignore[attr-defined]

    with patch("src.mcp.McpRegistry.McpToolAdapter"):
        disable_task = asyncio.create_task(registry.disable("test-server"))
        # Yield to let disable() reach the drain wait point.
        await asyncio.sleep(0)

        assert "terminate" not in terminate_order, "McpSandbox.terminate() was called before in-flight drain completed"

        # Simulate all in-flight calls completing.
        registry._in_flight_counts["test-server"] = 0  # type: ignore[index]
        drain_event.set()

        await disable_task

    assert "terminate" in terminate_order, "McpSandbox.terminate() was never called after drain"


# ---------------------------------------------------------------------------
# TC-REG-04  reload cycles disable then enable in order
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reload_cycles_disable_then_enable(registry: McpRegistry) -> None:
    """reload() must call disable() followed by enable() in strict sequence.

    Verifies ordering using a call-order recorder so that a reversed
    implementation would trigger an assertion failure.
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    call_order: list[str] = []

    async def mock_disable(name: str) -> None:
        """Record disable call."""
        call_order.append(f"disable:{name}")

    async def mock_enable(name: str) -> None:
        """Record enable call."""
        call_order.append(f"enable:{name}")

    registry.disable = mock_disable  # type: ignore[method-assign]
    registry.enable = mock_enable  # type: ignore[method-assign]

    await registry.reload("test-server")

    assert call_order == ["disable:test-server", "enable:test-server"], (
        f"Expected [disable, enable] order, got {call_order}"
    )


# ---------------------------------------------------------------------------
# TC-REG-05  get_client raises McpServerNotEnabled for unknown/stopped server
# ---------------------------------------------------------------------------


def test_get_client_raises_when_not_enabled(registry: McpRegistry) -> None:
    """get_client() raises McpServerNotEnabled when the named server is not running.

    Verifies that retrieving a client for a non-existent or stopped server
    raises the correct exception type rather than returning None or crashing.
    """
    with pytest.raises(McpServerNotEnabled):
        registry.get_client("missing-server")


# ---------------------------------------------------------------------------
# TC-REG-06  enable twice is idempotent (no second spawn)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_enable_already_enabled_is_idempotent(registry: McpRegistry) -> None:
    """Calling enable() on an already-running server does not spawn a second process.

    Either raises McpServerAlreadyEnabled or silently skips; either way
    McpSandbox.spawn must be called exactly once total.
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    mock_process = MagicMock()
    spawn_call_count = 0

    async def counting_spawn(_config: object) -> MagicMock:
        """Count how many times spawn is invoked."""
        nonlocal spawn_call_count
        spawn_call_count += 1
        return mock_process

    with (
        patch("src.mcp.McpRegistry.McpSandbox") as mock_sandbox_cls,
        patch("src.mcp.McpRegistry.McpClient") as mock_client_cls,
        patch("src.mcp.McpRegistry.McpToolAdapter"),
    ):
        mock_sandbox_cls.return_value.spawn = counting_spawn
        mock_client_cls.return_value.initialize = AsyncMock()
        mock_client_cls.return_value.list_tools = AsyncMock(return_value=[])

        await registry.enable("test-server")
        try:
            await registry.enable("test-server")
        except McpServerAlreadyEnabled:
            pass  # valid — raising is also acceptable idempotency

    assert spawn_call_count == 1, f"McpSandbox.spawn() called {spawn_call_count} times; expected exactly 1"


# ---------------------------------------------------------------------------
# TC-REG-07  list_servers returns a snapshot (mutation-safe)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_servers_returns_snapshot(registry: McpRegistry) -> None:
    """list_servers() returns a copy; mutating the returned list does not alter the registry.

    Verifies copy-on-return semantics: a second call to list_servers() after
    externally mutating the first result still returns the original count.
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    first_snapshot = registry.list_servers()
    assert len(first_snapshot) == 1

    # Mutate the returned list.
    first_snapshot.clear()

    second_snapshot = registry.list_servers()
    assert len(second_snapshot) == 1, "Registry internal state was modified by mutating the list_servers() return value"


# ---------------------------------------------------------------------------
# TC-REG-08  concurrent enable + disable is safe
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_concurrent_enable_disable_safe(registry: McpRegistry) -> None:
    """Concurrent enable() and disable() for the same server does not raise unhandled errors.

    Both operations may legitimately raise McpServerNotEnabled / McpServerAlreadyEnabled;
    what is NOT acceptable is an unhandled asyncio error or deadlock.
    """
    with patch("yaml.safe_load", return_value=[_SERVER_DICT]), patch("builtins.open"):
        await registry.load_config("mcp_servers.yml")

    mock_process = MagicMock()

    with (
        patch("src.mcp.McpRegistry.McpSandbox") as mock_sandbox_cls,
        patch("src.mcp.McpRegistry.McpClient") as mock_client_cls,
        patch("src.mcp.McpRegistry.McpToolAdapter"),
    ):
        mock_sandbox_cls.return_value.spawn = AsyncMock(return_value=mock_process)
        mock_sandbox_cls.return_value.terminate = AsyncMock()
        mock_client_cls.return_value.initialize = AsyncMock()
        mock_client_cls.return_value.list_tools = AsyncMock(return_value=[])

        results = await asyncio.gather(
            registry.enable("test-server"),
            registry.disable("test-server"),
            return_exceptions=True,
        )

    # Filter out acceptable domain exceptions; any other exception type is a failure.
    acceptable = (McpServerNotEnabled, McpServerAlreadyEnabled)
    unexpected = [r for r in results if isinstance(r, Exception) and not isinstance(r, acceptable)]
    assert not unexpected, f"Unexpected exceptions during concurrent operations: {unexpected}"


# ---------------------------------------------------------------------------
# TC-REG-09  reload unknown server raises McpServerNotFound
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reload_on_unknown_server_raises(registry: McpRegistry) -> None:
    """reload() raises McpServerNotFound when the named server does not exist in config.

    An empty registry has no configured servers; any reload attempt must
    immediately raise McpServerNotFound without spawning any process.
    """
    with pytest.raises(McpServerNotFound):
        await registry.reload("no-such-server")
