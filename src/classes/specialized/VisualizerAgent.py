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

"""Agent specializing in mapping and visualizing the internal dependencies of the Agent OS.
Inspired by system-design-visualizer and FalkorDB.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.agents.cognitive.context.engines.GraphContextEngine import GraphContextEngine
from src.logic.agents.cognitive.GraphMemoryAgent import GraphMemoryAgent

__version__ = VERSION

class VisualizerAgent(BaseAgent):
    """Maps relationships and handles Visual Workflow Export/Import (cc-wf-studio pattern)."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.graph_engine = GraphContextEngine(str(self.workspace_root))
        self.memory_agent: GraphMemoryAgent | None = None
        
        self._system_prompt = (
            "You are the Fleet Visualizer Agent. "
            "You follow the cc-wf-studio visual workflow format for export/import.\n"
            "This allows the PyAgent Fleet to interact with visual canvas-based builders."
        )

    @as_tool
    def spatial_reasoning(self, objects: list[dict[str, Any]], query: str) -> str:
        """
        Performs spatial reasoning on a list of objects in a 2D/3D space.
        Args:
            objects: List of objects with 'id', 'type', 'position' (x, y, z), and 'size'.
            query: Spatial query (e.g., 'Is agent A closer to tool B than tool C?').
        """
        logging.info(f"VISUALIZER: Performing spatial reasoning for query: {query}")
        
        # Simple heuristic or AI-based reasoning
        # For simplicity, we just format the objects for the LLM to reason about
        prompt = (
            f"Spatial Environment: {json.dumps(objects)}\n"
            f"Query: {query}\n"
            "Analyze the spatial relationships and provide a clear answer."
        )
        
        return self.think(prompt)

    @as_tool
    def video_grounding(self, frames: list[dict[str, Any]], event_query: str) -> dict[str, Any]:
        """
        Phase 58: Video Grounding.
        Analyzes a sequence of video frames to identify events or temporal relationships.
        Args:
            frames: List of frame metadata (timestamp, detected_objects).
            event_query: Query about an event (e.g., 'When did the human pick up the tool?').
        """
        logging.info(f"VISUALIZER: Performing video grounding for query: {event_query}")
        
        # Simulation: identify change between frames
        # For demonstration, we simply return a mocked temporal analysis
        return {
            "query": event_query,
            "event_start": frames[0]["timestamp"] if frames else 0,
            "confidence": 0.85,
            "detected_sequence": [f["detected_objects"] for f in frames],
            "conclusion": f"Analysis of {len(frames)} frames confirms intent for: {event_query}"
        }

    @as_tool
    def export_visual_workflow(self, workflow_name: str, tasks: list[dict[str, Any]]) -> str:
        """Exports a task sequence as a JSON visual workflow (cc-wf-studio format)."""
        logging.info(f"VISUALIZER: Exporting visual workflow '{workflow_name}'")
        
        nodes = []
        edges = []
        
        for i, task in enumerate(tasks):
            node_id = f"node_{i}"
            nodes.append({
                "id": node_id,
                "type": "agent_action",
                "data": {"label": task.get("title", f"Task {i}"), "agent": task.get("agent", "Generic")},
                "position": {"x": 100 * i, "y": 100 * i}
            })
            if i > 0:
                edges.append({
                    "id": f"edge_{i-1}_{i}",
                    "source": f"node_{i-1}",
                    "target": node_id,
                    "label": "sequence"
                })
        
        workflow_data = {
            "name": workflow_name,
            "version": "1.0.0",
            "canvas": {"nodes": nodes, "edges": edges}
        }
        
        output_path = Path(str(self.workspace_root)) / "config" / f"{workflow_name}_visual.json"
        with open(output_path, 'w') as f:
            json.dump(workflow_data, f, indent=2)
            
        return f"Successfully exported visual workflow to {output_path}"

    @as_tool
    def import_visual_workflow(self, file_name: str) -> dict[str, Any]:
        """Imports a JSON visual workflow and converts it to a Task Planner sequence."""
        logging.info(f"VISUALIZER: Importing visual workflow '{file_name}'")
        input_path = Path(str(self.workspace_root)) / "config" / file_name
        
        if not input_path.exists():
            return {"error": f"File {file_name} not found in config/"}
            
        with open(input_path) as f:
            data = json.load(f)
            
        # Convert canvas nodes to fleet tasks
        tasks = []
        for node in data.get("canvas", {}).get("nodes", []):
            tasks.append({
                "title": node["data"]["label"],
                "agent": node["data"]["agent"],
                "status": "pending"
            })
            
        return {"workflow_name": data.get("name"), "tasks": tasks}

    def set_memory_agent(self, agent: GraphMemoryAgent) -> None:
        """Connects a GraphMemoryAgent for knowledge visualization."""
        self.memory_agent = agent

    @as_tool
    def visualize_knowledge_graph(self) -> str:
        """Generates a Mermaid graph from the GraphMemory triples."""
        if not self.memory_agent:
            return "Error: No GraphMemoryAgent connected to VisualizerAgent."
            
        relationships = self.memory_agent.relationships
        if not relationships:
            return "## 🧠 Knowledge Graph\n\nNo relationships found in memory."
            
        lines = ["graph LR"]
        for rel in relationships:
            s = rel['subject'].replace(" ", "_")
            p = rel['predicate'].replace(" ", "_")
            o = rel['object'].replace(" ", "_")
            lines.append(f"    {s} -- {p} --> {o}")
            
        return "## 🧠 Knowledge Graph\n\n```mermaid\n" + "\n".join(lines) + "\n```"

    @as_tool
    def generate_fleet_map(self) -> str:
        """Generates a Mermaid class diagram of the entire agent fleet."""
        logging.info("VisualizerAgent generating fleet map...")
        
        # We manually build the core fleet map for now
        diagram = [
            "classDiagram",
            "    class BaseAgent { +improve_content() }",
            "    class FleetManager { +execute_workflow() }",
            "    class TaskPlannerAgent { +create_plan() }",
            "    class KnowledgeAgent { +query_knowledge() }",
            "    class SecurityGuardAgent { +improve_content() }",
            "",
            "    FleetManager --> BaseAgent : manages",
            "    TaskPlannerAgent --|> BaseAgent : inherits",
            "    KnowledgeAgent --|> BaseAgent : inherits",
            "    SecurityGuardAgent --|> BaseAgent : inherits",
            "    MetaOrchestratorAgent --> FleetManager : uses"
        ]
        
        return "## 🗺️ Fleet Architecture Map\n\n```mermaid\n" + "\n".join(diagram) + "\n```"

    @as_tool
    def generate_call_graph(self, filter_term: str = "") -> str:
        """Generates a Mermaid flowchart of function calls based on the graph engine."""
        self.graph_engine.scan_project()
        symbols = self.graph_engine.symbols
        
        lines = ["graph TD"]
        count = 0
        for file, data in symbols.items():
            if filter_term and filter_term not in file:
                continue
            
            clean_file = file.replace("\\", "/").split("/")[-1]
            for call in data.get("calls", []):
                if count > 20:
                    break # Keep it readable
                lines.append(f"    {clean_file} --> {call}")
                count += 1
                
        return "## 🔗 Code Call Graph\n\n```mermaid\n" + "\n".join(lines) + "\n```"

    def generate_3d_swarm_data(self) -> dict[str, Any]:
        """
        Generates a 3D-compatible dataset for force-directed swarm visualization.
        Schema compatible with Force-Directed Graph libraries.
        """
        nodes = [
            {"id": "FleetManager", "group": 1, "size": 10},
            {"id": "SecurityAudit", "group": 2, "size": 5},
            {"id": "PrivacyGuard", "group": 2, "size": 5},
            {"id": "CoderAgent", "group": 3, "size": 7},
            {"id": "ByzantineConsensus", "group": 4, "size": 6}
        ]
        links = [
            {"source": "FleetManager", "target": "SecurityAudit", "value": 1},
            {"source": "FleetManager", "target": "CoderAgent", "value": 1},
            {"source": "SecurityAudit", "target": "PrivacyGuard", "value": 0.5},
            {"source": "CoderAgent", "target": "ByzantineConsensus", "value": 0.8}
        ]
        
        return {
            "format": "v1-3d-swarm",
            "nodes": nodes,
            "links": links,
            "metadata": {
                "generated_at": time.time(),
                "node_count": len(nodes)
            }
        }

    def improve_content(self, prompt: str) -> str:
        """Visualizes the workspace by default."""
        return self.generate_call_graph()