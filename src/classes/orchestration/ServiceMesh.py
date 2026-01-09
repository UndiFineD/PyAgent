#!/usr/bin/env python3

"""Service Mesh for synchronizing tools and capabilities across distributed fleet nodes."""

import logging
import json
from typing import Dict, List, Any, Optional
from src.classes.orchestration.SignalRegistry import SignalRegistry

class ServiceMesh:
    """Manages cross-node tool discovery and capability synchronization."""
    
    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.known_nodes: Dict[str, List[str]] = {} # URL -> List of tool names
        self.local_tools: List[str] = []
        
        # Subscribe to tool registration events
        self.fleet.signals.subscribe("TOOL_REGISTERED", self._on_tool_registered)
        
    def _on_tool_registered(self, payload: Dict[str, Any]):
        """Handler for local tool registration."""
        tool_name = payload.get("tool_name")
        if tool_name and tool_name not in self.local_tools:
            self.local_tools.append(tool_name)
            self._broadcast_capability(tool_name)

    def _broadcast_capability(self, tool_name: str):
        """Informs remote nodes about a new local tool (Stub for P2P/PubSub)."""
        logging.info(f"MESH: Broadcasting local capability '{tool_name}' to fleet.")
        # In Phase 16, this could use the PublicAPIEngine to notify registered remote nodes.
        for node in getattr(self.fleet, 'remote_nodes', []):
            logging.debug(f"MESH: Syncing '{tool_name}' with {node}")

    def sync_with_remote(self, node_url: str):
        """Fetches available tools from a remote node."""
        try:
            # Simulated call to remote node's discovery endpoint
            remote_tools = ["remote_analyzer", "cloud_scaler", "global_context_shard"] 
            self.known_nodes[node_url] = remote_tools
            for tool in remote_tools:
                # Wrap lambda to give it a name and docstring for registry extraction
                def remote_proxy(**kwargs):
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

    def get_mesh_status(self) -> Dict[str, Any]:
        """Returns stats about the mesh."""
        return {
            "local_tools": len(self.local_tools),
            "remote_nodes": len(self.known_nodes),
            "total_reachable_tools": sum(len(tools) for tools in self.known_nodes.values()) + len(self.local_tools)
        }
