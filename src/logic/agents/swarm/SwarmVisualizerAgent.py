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

from __future__ import annotations
from src.core.base.version import VERSION
import time
from typing import Dict, Any

__version__ = VERSION

class SwarmVisualizerAgent:
    """
    Generates topological maps and visualizations of agent interactions.
    Tracks message flows, agent dependencies, and swarm health metrics.
    """
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.interaction_log = [] # List of (from_agent, to_agent, message_type, timestamp)
        self.agent_positions = {} # agent_id -> (x, y)

    def log_interaction(self, from_agent: str, to_agent: str, message_type: str) -> None:
        """Logs an interaction between two agents."""
        self.interaction_log.append({
            "from": from_agent,
            "to": to_agent,
            "type": message_type,
            "timestamp": time.time()
        })
        # Keep log size manageable
        if len(self.interaction_log) > 1000:
            self.interaction_log.pop(0)

    def generate_topology_map(self) -> dict[str, Any]:
        """Generates a graph-based representation of the swarm topology."""
        nodes = set()
        edges = []
        
        for interaction in self.interaction_log:
            nodes.add(interaction["from"])
            nodes.add(interaction["to"])
            edges.append({
                "source": interaction["from"],
                "target": interaction["to"],
                "type": interaction["type"]
            })
            
        return {
            "nodes": list(nodes),
            "edges": edges,
            "timestamp": time.time(),
            "complexity_score": len(edges) / max(1, len(nodes))
        }

    def update_agent_position(self, agent_id: str, x: float, y: float) -> None:
        """Updates the visual position of an agent in the topology."""
        self.agent_positions[agent_id] = {"x": x, "y": y}

    def get_visualization_data(self) -> dict[str, Any]:
        """Returns all data needed for a real-time visualization dashboard."""
        return {
            "topology": self.generate_topology_map(),
            "positions": self.agent_positions,
            "metrics": {
                "total_interactions": len(self.interaction_log),
                "active_agents": len(self.agent_positions)
            }
        }