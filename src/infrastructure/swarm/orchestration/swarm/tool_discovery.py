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

"""
Tool discovery.py module.
"""

import logging
from typing import Any, Dict, Optional

from src.infrastructure.engine.models.similarity import \
    EmbeddingSimilarityService

logger = logging.getLogger(__name__)


class AutonomousToolDiscovery:
    """
    Dynamically expands swarm capabilities by discovering MCP tools (Phase 87).
    Allows the swarm to 'learn' about new external APIs without manual registration.
    """

    def __init__(self, mcp_agent: Any, similarity_service: EmbeddingSimilarityService):
        self.mcp_agent = mcp_agent
        self.similarity_service = similarity_service
        # Cached tool descriptions and their embeddings
        self.tool_index: Dict[str, Dict[str, Any]] = {}

    async def refresh_tool_index(self):
        """Fetches all tools from all MCP servers and indexes them semantically."""
        # 1. Get server list
        await self.mcp_agent.list_mcp_servers()
        # Mocking parsing for now - in production, MCPAgent should return structured data
        # For Phase 87, we'll assume a list of servers to probe
        servers = ["github", "brave_search", "google_maps"]  # Mock probe list

        for server in servers:
            try:
                # Mock calling a list_tools tool on the server
                # tools = await self.mcp_agent.call_mcp_tool(server, "list_tools", {})
                # For this implementation, we simulate discovered tools:
                simulated_tools = [
                    {"name": f"{server}_search", "desc": f"Search using {server} API"},
                    {"name": f"{server}_mutate", "desc": f"Modify resources on {server}"},
                ]

                for tool in simulated_tools:
                    tool_id = f"{server}:{tool['name']}"
                    emb = await self.similarity_service.get_embedding(tool["desc"])
                    self.tool_index[tool_id] = {
                        "server": server,
                        "name": tool["name"],
                        "desc": tool["desc"],
                        "embedding": emb,
                    }
            except Exception as e:
                logger.error(f"Failed to index tools for MCP server {server}: {e}")

    async def find_external_tool(self, task_prompt: str, threshold: float = 0.7) -> Optional[Dict[str, Any]]:
        """Finds an MCP tool that matches the semantic requirements of a task."""
        if not self.tool_index:
            await self.refresh_tool_index()

        task_emb = await self.similarity_service.get_embedding(task_prompt)

        best_tool = None
        best_score = -1.0

        for tool_id, data in self.tool_index.items():
            score = await self.similarity_service.compute_similarity(task_emb, data["embedding"])
            if score > best_score:
                best_score = score
                best_tool = data

        if best_tool and best_score >= threshold:
            logger.info(
                f"[Phase 87] Tool Discovery: Found external tool '{best_tool['name']}' with score {best_score:.3f}"
            )
            return {"tool_id": best_tool["name"], "server": best_tool["server"], "score": best_score}

        return None
