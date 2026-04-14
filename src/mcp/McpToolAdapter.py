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
"""Bridges MCP server tools into the PyAgent tool registry.

:class:`McpToolAdapter` translates the per-server flat tool list returned by
:class:`~src.mcp.McpClient.McpClient` into namespaced ``Tool`` entries in a
shared registry dict using the scheme ``mcp::<server_name>::<tool_name>``.

The adapter never interacts with ``src.tools.tool_registry._REGISTRY`` directly;
instead it operates on an injected ``registry_ref`` dict so that unit tests can
use a plain in-memory dict and the registry can be wired at construction time.
"""

from __future__ import annotations

from typing import Any, Callable

from src.mcp.exceptions import McpToolNameCollision
from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
from src.mcp.McpSandbox import McpSandbox
from src.mcp.McpServerConfig import McpServerConfig
from src.tools.tool_registry import Tool

__all__ = ["McpToolAdapter"]


class McpToolAdapter:
    """Registers and deregisters MCP server tools in a shared registry dict.

    Args:
        registry_ref: A mutable ``dict`` that acts as the live tool registry.
            The adapter reads from and writes to this dict directly.  Pass
            ``src.tools.tool_registry._REGISTRY`` for production use or a
            fresh ``{}`` in tests.

    """

    def __init__(self, registry_ref: dict[str, Any]) -> None:
        """Initialise the adapter with a reference to the shared registry.

        Args:
            registry_ref: The live registry dict.  The adapter stores all
                registered tool entries here and removes them on deregister.

        """
        self._registry = registry_ref
        # Maps server_name → set of namespaced keys owned by that server.
        self._server_tools: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    async def register_server_tools(
        self,
        server_name: str,
        client: McpClient,
        sandbox: McpSandbox,
        config: McpServerConfig,
    ) -> int:
        """Discover and register all tools exposed by an MCP server.

        Calls :meth:`~src.mcp.McpClient.McpClient.list_tools`, converts each
        definition to a namespaced :class:`~src.tools.tool_registry.Tool`, and
        inserts it into ``registry_ref``.

        Args:
            server_name: The unique server slug (e.g. ``"github"``).  Used as
                the namespace prefix: ``mcp::<server_name>::<tool_name>``.
            client: A connected :class:`~src.mcp.McpClient.McpClient` for this
                server.
            sandbox: The :class:`~src.mcp.McpSandbox.McpSandbox` owning the
                server process (stored for future hot-reload).
            config: Server configuration (timeout, etc.).

        Returns:
            The number of tools successfully registered.

        Raises:
            McpToolNameCollision: If any namespaced tool name already exists in
                ``registry_ref`` (pre-existing non-MCP tool or duplicate server
                registration).

        """
        tool_defs: list[McpToolDefinition] = await client.list_tools()
        registered: list[str] = []

        for defn in tool_defs:
            namespaced_name = f"mcp::{server_name}::{defn.name}"
            if namespaced_name in self._registry:
                raise McpToolNameCollision(f"Tool '{namespaced_name}' is already registered in the registry")

            tool = self._build_tool(server_name, defn, client, config)
            self._registry[namespaced_name] = tool
            registered.append(namespaced_name)

        self._server_tools[server_name] = set(registered)
        return len(registered)

    async def deregister_server_tools(self, server_name: str) -> int:
        """Remove all tools registered under *server_name* from the registry.

        Uses the internal bookkeeping map so only keys owned by this server are
        removed — other servers' entries are never touched.

        Args:
            server_name: The unique server slug whose tools should be removed.

        Returns:
            The number of tools removed.  Returns ``0`` if the server was never
            registered (silent no-op).

        """
        owned: set[str] | None = self._server_tools.pop(server_name, None)
        if owned is None:
            return 0
        for key in owned:
            self._registry.pop(key, None)
        return len(owned)

    # ------------------------------------------------------------------
    # Static conversion helper
    # ------------------------------------------------------------------

    @staticmethod
    def tool_definition_to_spec(
        server_name: str,
        defn: McpToolDefinition,
    ) -> tuple[str, Callable[..., Any], str]:
        """Convert an MCP tool definition to a PyAgent tool-spec 3-tuple.

        The returned ``async_main`` is an async callable compatible with the
        :data:`src.tools.tool_registry.ToolMain` signature.  The actual
        ``McpClient`` is not bound here (use :meth:`register_server_tools` for
        that); the callable returned is a structural prototype used for schema
        introspection.

        Args:
            server_name: Server namespace slug (e.g. ``"fs"``).
            defn: The tool definition as returned by
                :meth:`src.mcp.McpClient.McpClient.list_tools`.

        Returns:
            A 3-tuple ``(namespaced_name, async_main, description)`` where:

            - ``namespaced_name``: ``"mcp::<server_name>::<tool_name>"``
            - ``async_main``: An async callable with signature
              ``(args: list[str] | None = None) -> int``.
            - ``description``: Human-readable label referencing the server and
              tool name.

        """
        namespaced_name = f"mcp::{server_name}::{defn.name}"
        description = f"[{server_name}] {defn.description}"

        async def async_main(args: list[str] | None = None) -> int:  # noqa: ARG001
            """Structural prototype; real closure built by register_server_tools.

            Args:
                args: CLI-style argument list (unused in prototype).

            Returns:
                Always returns 0.

            """
            return 0

        return namespaced_name, async_main, description

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_tool(
        server_name: str,
        defn: McpToolDefinition,
        client: McpClient,
        config: McpServerConfig,
    ) -> Tool:
        """Build a :class:`~src.tools.tool_registry.Tool` whose main calls the server.

        The closure captures *client* and the un-namespaced *tool_name* by
        value so that each tool independently dispatches to the correct server.

        Args:
            server_name: The namespace slug (e.g. ``"fs"``).
            defn: Tool definition providing name and description.
            client: Connected :class:`~src.mcp.McpClient.McpClient` for this
                server.
            config: Used to read ``timeout_seconds`` for future per-call
                override support.

        Returns:
            A frozen :class:`~src.tools.tool_registry.Tool` instance whose
            ``main`` callable dispatches to the MCP server.

        """
        namespaced_name = f"mcp::{server_name}::{defn.name}"
        description = f"[{server_name}] {defn.description}"
        tool_name: str = defn.name  # captured by closure

        async def async_main(args: list[str] | None = None) -> int:
            """Dispatch the tool call to the MCP server over JSON-RPC stdin/stdout.

            Args:
                args: CLI-style argument list.  Currently forwarded as an
                    empty arguments dict to the server; structured parsing
                    will be added in a later phase.

            Returns:
                0 on a successful (non-error) tool result.

            """
            result: McpToolResult = await client.call_tool(tool_name, {})
            return 1 if result.is_error else 0

        return Tool(
            name=namespaced_name,
            main=async_main,
            description=description,
        )
