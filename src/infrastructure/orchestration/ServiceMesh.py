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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Service Mesh for synchronizing tools and capabilities across distributed fleet nodes."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Any

__version__ = VERSION




class ServiceMesh:
    """Manages cross-node tool discovery and capability synchronization."""

    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.known_nodes: dict[str, list[str]] = {}  # URL -> List of tool names
        self.local_tools: list[str] = []

        # Subscribe to tool registration events
        self.fleet.signals.subscribe("TOOL_REGISTERED", self._on_tool_registered)

    def _on_tool_registered(self, payload: dict[str, Any]) -> None:
        """Handler for local tool registration."""
        tool_name = payload.get("tool_name")
        if tool_name and tool_name not in self.local_tools:
            self.local_tools.append(tool_name)
            self._broadcast_capability(tool_name)

    def _broadcast_capability(self, tool_name: str) -> None:
        """Informs remote nodes about a new local tool (Stub for P2P/PubSub)."""
        logging.info(f"MESH: Broadcasting local capability '{tool_name}' to fleet.")
        # In Phase 16, this could use the PublicAPIEngine to notify registered remote nodes.
        for node in getattr(self.fleet, 'remote_nodes', []):
            logging.debug(f"MESH: Syncing '{tool_name}' with {node}")

    def sync_with_remote(self, node_url: str) -> None:
        """Fetches available tools from a remote node."""
        try:
            # Simulated call to remote node's discovery endpoint
            remote_tools = ["remote_analyzer", "cloud_scaler", "global_context_shard"]
            self.known_nodes[node_url] = remote_tools
            for tool in remote_tools:
                # Wrap lambda to give it a name and docstring for registry extraction
                def remote_proxy(**kwargs: Any) -> str:
                    """Remote tool proxy."""
                    return f"Remote proxy call to {tool} at {node_url}"
                remote_proxy.__name__ = f"{tool}_at_{node_url.replace(':', '_').replace('/', '_').replace('.', '_')}"

                self.fleet.registry.register_tool(
                    owner_name=f"RemoteNode:{node_url}",
                    func=remote_proxy,
                    category="remote"
                )
            logging.info(f"MESH: Synchronized {len(remote_tools)} tools from {node_url}")
        except Exception as e:
            logging.error(f"MESH: Failed to sync with {node_url}: {e}")

    def get_mesh_status(self) -> dict[str, Any]:
        """Returns stats about the mesh."""
        return {
            "local_tools": len(self.local_tools),
            "remote_nodes": len(self.known_nodes),
            "total_reachable_tools": sum(len(tools) for tools in self.known_nodes.values()) + len(self.local_tools)
        }
