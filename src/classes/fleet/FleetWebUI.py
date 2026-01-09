#!/usr/bin/env python3

"""Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.
"""

import json
import logging
from typing import Dict, List, Any

class FleetWebUI:
    """Provides backend support for the Fleet visualization dashboard."""

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.generative_registry: Dict[str, Dict[str, Any]] = {} # Tambo Pattern

    def register_generative_component(self, name: str, description: str, props_schema: Dict[str, Any]) -> str:
        """Registers a UI component that the AI can choose to render dynamically (Tambo Pattern)."""
        self.generative_registry[name] = {
            "description": description,
            "props_schema": props_schema,
            "type": "generative"
        }
        logging.info(f"Registered generative UI component: {name}")

    def suggest_ui_components(self, task_result: str) -> List[Dict[str, Any]]:
        """AI decides which components to render based on the task output (Tambo Pattern)."""
        suggestions = []
        for name, metadata in self.generative_registry.items():
            if metadata["description"].lower() in task_result.lower():
                suggestions.append({"component": name, "props": {}}) # Simplified
        return suggestions

    def get_fleet_topology(self) -> str:
        """Returns a graph representation of the fleet for Mermaid/D3 visualization."""
        nodes = []
        links = []
        
        for name, agent in self.fleet.agents.items():
            nodes.append({"id": name, "type": "agent", "model": getattr(agent, "model", "unknown")})
            
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

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Returns a snapshot of fleet performance for real-time charts."""
        return self.fleet.telemetry.get_summary()

    def list_workspace_files(self, sub_path: str = ".") -> Dict[str, Any]:
        """Backend for the File Explorer with Preview.
        Returns directory structure and file metadata.
        """
        from pathlib import Path
        base = Path(self.fleet.workspace_root) / sub_path
        if not base.exists():
            return {"error": f"Path {sub_path} not found"}
            
        items = []
        for item in base.iterdir():
            items.append({
                "name": item.name,
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0,
                "extension": item.suffix if item.is_file() else "",
                "preview": self._get_preview(item) if item.is_file() else None
            })
        return {"path": str(sub_path), "items": items}

    def _get_preview(self, file_path: "Path") -> str:
        """Generates a small text preview for files."""
        try:
            if file_path.suffix in [".py", ".md", ".txt", ".json", ".yaml"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read(500) + "..."
            return "[No Preview Available]"
        except Exception:
            return "[Error Reading Preview]"

    def get_workflow_designer_state(self) -> Dict[str, Any]:
        """Returns the available nodes and signals for the Graphical Workflow Designer."""
        available_agents = []
        for name, agent in self.fleet.agents.items():
            methods = [m for m in dir(agent) if not m.startswith("_") and callable(getattr(agent, m))]
            available_agents.append({
                "name": name,
                "actions": methods,
                "capabilities": getattr(agent, "capabilities", [])
            })
            
        return {
            "agents": available_agents,
            "triggers": ["HTTP_REQUEST", "SCHEDULE", "SIGNAL_EMITTED"],
            "v_connectors": ["sequential", "parallel", "conditional"]
        }

    def get_multi_fleet_manager(self) -> Dict[str, Any]:
        """Returns status of multiple fleets (local and remote)."""
        return {
            "local_fleet": {
                "agents": len(self.fleet.agents),
                "status": "active"
            },
            "remote_nodes": self.fleet.remote_nodes,
            "mesh_status": self.fleet.mesh.get_mesh_status() if hasattr(self.fleet, "mesh") else "Unknown"
        }
