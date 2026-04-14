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
"""MCP server lifecycle registry.

:class:`McpRegistry` owns the startup, shutdown, hot-reload, and status
lifecycle for all enabled MCP server subprocesses.  It reads configuration
from ``mcp_servers.yml``, spawns sandboxed subprocesses via
:class:`~src.mcp.McpSandbox.McpSandbox`, establishes JSON-RPC clients via
:class:`~src.mcp.McpClient.McpClient`, and registers server tools into the
PyAgent tool registry via :class:`~src.mcp.McpToolAdapter.McpToolAdapter`.

Exported symbols:
    McpServerStatus: Enum describing the lifecycle state of one server.
    McpRegistry:     The central lifecycle manager.
"""

from __future__ import annotations

import asyncio
from enum import Enum

import yaml

from src.mcp.exceptions import (
    McpServerAlreadyEnabled,
    McpServerNotEnabled,
    McpServerNotFound,
)
from src.mcp.McpClient import McpClient
from src.mcp.McpSandbox import McpSandbox
from src.mcp.McpServerConfig import McpServerConfig
from src.mcp.McpToolAdapter import McpToolAdapter

__all__ = ["McpRegistry", "McpServerStatus"]


class McpServerStatus(Enum):
    """Lifecycle state of a single MCP server.

    Attributes:
        STOPPED: Server is configured but not running.
        STARTING: Server is spawning; not yet ready for tool calls.
        RUNNING: Server subprocess is live and tools are registered.
        STOPPING: Server is draining in-flight calls before shutdown.
        FAILED: Server stopped unexpectedly and exceeded restart attempts.

    """

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


class McpRegistry:
    """Central lifecycle manager for external MCP server subprocesses.

    Responsibilities:
    - Parse ``mcp_servers.yml`` into :class:`~src.mcp.McpServerConfig.McpServerConfig`
      instances.
    - Spawn, initialise, and track per-server
      :class:`~src.mcp.McpSandbox.McpSandbox` and
      :class:`~src.mcp.McpClient.McpClient` pairs.
    - Register / deregister server tools via
      :class:`~src.mcp.McpToolAdapter.McpToolAdapter`.
    - Hot-reload individual servers without disrupting others.
    - Provide thread-safe ``enable`` / ``disable`` idempotency via per-server
      asyncio events and in-flight counters.
    """

    def __init__(self) -> None:
        """Initialise an empty registry with no configured servers."""
        # Keyed by config.name
        self._configs: dict[str, McpServerConfig] = {}
        self._sandboxes: dict[str, McpSandbox] = {}
        self._clients: dict[str, McpClient] = {}
        self._processes: dict[str, asyncio.subprocess.Process] = {}
        self._status: dict[str, McpServerStatus] = {}
        self._drain_events: dict[str, asyncio.Event] = {}
        self._in_flight_counts: dict[str, int] = {}
        self._adapter = McpToolAdapter(registry_ref={})
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    async def load_config(self, path: str) -> None:
        """Parse ``mcp_servers.yml`` and populate the internal config map.

        Each top-level entry under the ``mcp_servers`` key is converted to a
        :class:`~src.mcp.McpServerConfig.McpServerConfig`.  Existing runtime
        state (running servers) is NOT affected; only the config map changes.

        Args:
            path: Filesystem path to the YAML configuration file.

        """
        with open(path) as fh:
            raw = yaml.safe_load(fh)

        entries = raw if isinstance(raw, list) else raw.get("mcp_servers", [])
        for entry in entries:
            config = McpServerConfig.from_dict(entry)
            self._configs[config.name] = config
            if config.name not in self._status:
                self._status[config.name] = McpServerStatus.STOPPED

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def list_servers(self) -> list[McpServerConfig]:
        """Return a snapshot of all configured server configs.

        Returns:
            A new list so callers cannot mutate the registry's internal state.

        """
        return list(self._configs.values())

    def get_client(self, name: str) -> McpClient:
        """Return the live :class:`~src.mcp.McpClient.McpClient` for a running server.

        Args:
            name: The unique server slug.

        Returns:
            The connected :class:`~src.mcp.McpClient.McpClient` instance.

        Raises:
            McpServerNotEnabled: If the server is not currently running.

        """
        client = self._clients.get(name)
        if client is None:
            raise McpServerNotEnabled(f"Server '{name}' is not running; call enable() first")
        return client

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def enable(self, name: str) -> None:
        """Start a configured server and register its tools.

        Spawns the sandbox subprocess, runs the McpClient initialise
        handshake, and registers all discovered tools into the tool registry
        via :class:`~src.mcp.McpToolAdapter.McpToolAdapter`.

        Args:
            name: The unique server slug to enable.

        Raises:
            McpServerNotFound: If *name* has not been loaded via
                :meth:`load_config`.
            McpServerAlreadyEnabled: If the server is already running.

        """
        if name not in self._configs:
            raise McpServerNotFound(f"Server '{name}' is not configured")

        async with self._lock:
            current = self._status.get(name, McpServerStatus.STOPPED)
            if current == McpServerStatus.RUNNING:
                raise McpServerAlreadyEnabled(f"Server '{name}' is already running")

            self._status[name] = McpServerStatus.STARTING

        config = self._configs[name]
        sandbox = McpSandbox()
        process = await sandbox.spawn(config)

        client = McpClient(process=process, config=config)
        await client.initialize()

        self._sandboxes[name] = sandbox
        self._processes[name] = process
        self._clients[name] = client
        self._drain_events[name] = asyncio.Event()
        self._drain_events[name].set()  # no in-flight yet
        self._in_flight_counts[name] = 0

        await self._adapter.register_server_tools(name, client, sandbox, config)

        async with self._lock:
            self._status[name] = McpServerStatus.RUNNING

    async def disable(self, name: str) -> None:
        """Drain in-flight calls and shut down a running server.

        Waits until the server has no active in-flight tool calls, deregisters
        its tools, then terminates the subprocess.

        Args:
            name: The unique server slug to disable.

        Raises:
            McpServerNotEnabled: If *name* is not currently running.

        """
        current = self._status.get(name)
        if current != McpServerStatus.RUNNING:
            raise McpServerNotEnabled(f"Server '{name}' is not running")

        async with self._lock:
            self._status[name] = McpServerStatus.STOPPING

        # Drain: wait until in-flight count reaches zero.
        drain_event = self._drain_events.get(name)
        if drain_event is not None:
            while self._in_flight_counts.get(name, 0) > 0:
                drain_event.clear()
                await drain_event.wait()

        await self._adapter.deregister_server_tools(name)

        process = self._processes.pop(name, None)
        sandbox = self._sandboxes.pop(name, None)
        if sandbox is not None and process is not None:
            await sandbox.terminate(process)

        self._clients.pop(name, None)
        self._processes.pop(name, None)
        self._drain_events.pop(name, None)
        self._in_flight_counts.pop(name, None)

        async with self._lock:
            self._status[name] = McpServerStatus.STOPPED

    async def reload(self, name: str) -> None:
        """Hot-reload a server: disable then re-enable in strict sequence.

        Args:
            name: The unique server slug to reload.

        Raises:
            McpServerNotFound: If *name* has not been loaded via
                :meth:`load_config`.

        """
        if name not in self._configs:
            raise McpServerNotFound(f"Server '{name}' is not configured; cannot reload")
        await self.disable(name)
        await self.enable(name)
