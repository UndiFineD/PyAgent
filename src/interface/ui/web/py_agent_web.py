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


"""Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .agent_bar import AgentBar

__version__ = VERSION


class FleetWebUI:
    """Provides backend support for the Fleet visualization dashboard."""

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.generative_registry: dict[str, dict[str, Any]] = {}  # Tambo Pattern
        self.agent_bar = AgentBar()
        self._register_default_components()

    def _register_default_components(self):
        """Registers system default components."""
        self.register_generative_component(
            "AgentBar",
            "Floating real-time metrics and multimodal control bar.",
            {"status": "string", "metrics": "object"},
        )

    def register_generative_component(self, name: str, description: str, props_schema: dict[str, Any]) -> str:
        """Registers a UI component that the AI can choose to render dynamically (Tambo Pattern)."""
        self.generative_registry[name] = {
            "description": description,
            "props_schema": props_schema,
            "type": "generative",
        }
        logging.info(f"Registered generative UI component: {name}")

    def suggest_ui_components(self, task_result: str) -> list[dict[str, Any]]:
        """AI decides which components to render based on the task output (Tambo Pattern)."""
        suggestions = []
        for name, metadata in self.generative_registry.items():
            if metadata["description"].lower() in task_result.lower():
                suggestions.append({"component": name, "props": {}})  # Simplified
        return suggestions

    def get_fleet_topology(self) -> str:
        """Returns a graph representation of the fleet for Mermaid/D3 visualization."""
        nodes = []
        links: list[Any] = []

        for name, agent in self.fleet.agents.items():
            nodes.append(
                {
                    "id": name,
                    "type": "agent",
                    "model": getattr(agent, "model", "unknown"),
                }
            )

        return json.dumps({"nodes": nodes, "links": links}, indent=2)

    def generate_workflow_graph(self, workflow_state: Any) -> str:
        """Generates a Mermaid graph for a specific workflow's progress."""
        if not workflow_state:
            return "graph TD\n  Empty[No Active Workflow]"

        mermaid_lines = ["graph LR"]
        history = workflow_state.history

        last_node = "START"
        for i, entry in enumerate(history):
            node_id = f"step_{i}_{entry['agent']}"
            mermaid_lines.append(f"  {last_node} --> {node_id}")
            mermaid_lines.append(f"  {node_id}[{entry['agent']}: {entry['action']}]")
            last_node = node_id

        return "\n".join(mermaid_lines)

    def get_metrics_snapshot(self) -> dict[str, Any]:
        """Returns a snapshot of fleet performance for real-time charts."""
        return self.fleet.telemetry.get_summary()

    def list_workspace_files(self, sub_path: str = ".") -> dict[str, Any]:
        """Backend for the File Explorer with Preview.
        Returns directory structure and file metadata.
        """

        base = Path(self.fleet.workspace_root) / sub_path
        if not base.exists():
            return {"error": f"Path {sub_path} not found"}

        items = []
        for item in base.iterdir():
            items.append(
                {
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else 0,
                    "extension": item.suffix if item.is_file() else "",
                    "preview": self._get_preview(item) if item.is_file() else None,
                }
            )
        return {"path": str(sub_path), "items": items}

    def _get_preview(self, file_path: Path) -> str:
        """Generates a small text preview for files."""
        try:
            if file_path.suffix in [".py", ".md", ".txt", ".json", ".yaml"]:
                with open(file_path, encoding="utf-8") as f:
                    return f.read(500) + "..."
            return "[No Preview Available]"
        except (RuntimeError, ValueError) as e:
            pass
        except BaseException as e:
            pass
            import traceback
            print(f"Error reading preview for {file_path}: {e}\n{traceback.format_exc()}")
            return "[Error Reading Preview]"

    def get_workflow_designer_state(self) -> dict[str, Any]:
        """Returns the available nodes and signals for the Graphical Workflow Designer."""
        available_agents = []
        for name, agent in self.fleet.agents.items():
            methods = [m for m in dir(agent) if not m.startswith("_") and callable(getattr(agent, m))]
            available_agents.append(
                {
                    "name": name,
                    "actions": methods,
                    "capabilities": getattr(agent, "capabilities", []),
                }
            )

        return {
            "agents": available_agents,
            "triggers": ["HTTP_REQUEST", "SCHEDULE", "SIGNAL_EMITTED"],
            "v_connectors": ["sequential", "parallel", "conditional"],
        }

    def get_multi_fleet_manager(self) -> dict[str, Any]:
        """Returns status of multiple fleets (local and remote)."""
        return {
            "local_fleet": {"agents": len(self.fleet.agents), "status": "active"},
            "remote_nodes": self.fleet.remote_nodes,
            "mesh_status": self.fleet.mesh.get_mesh_status() if hasattr(self.fleet, "mesh") else "Unknown",
        }
