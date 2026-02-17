#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# "Context visualization tools for Cognitive agents."This module provides functionality to generate dependency graphs and hierarchy
visualizations for agent contexts and their inter-relationships.
"""


from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.models.visualization_data import (
    VisualizationData,
)
from src.logic.agents.cognitive.context.models.visualization_type import (
    VisualizationType,
)

__version__ = VERSION




class ContextVisualizer:
    "Visualizes context relationships."
    Creates visual representations of context dependencies and hierarchies.

    Example:
        >>> visualizer = ContextVisualizer()
#         >>> data = visualizer.create_dependency_graph(contexts)

    def __init__(
        self, viz_type: VisualizationType = VisualizationType.DEPENDENCY_GRAPH
    ) -> None:
        "Initialize context" visualizer."
        Args:
            viz_type: The default visualization type to use.
        self.viz_type: VisualizationType = viz_type
        self.nodes: list[dict[str, Any]] = []
        self.edges: list[tuple[str, str]] = []
#         self.layout: str = "hierarchical"
    def set_type(self, viz_type: VisualizationType) -> None:
        "Set the visualization type."
        Args:
            viz_type: The visualization type to set.
        self.viz_type = viz_type

    def add_node(self, node_id: str, metadata: dict[str, Any] | None = None) -> None:
        "Add a node to the visualization."
        Args:
            node_id: Unique identifier for the node.
            metadata: Optional metadata associated with the node.
 "       if metadata is None:"            metadata = {}
        self.nodes.append({"id": node_id, **metadata})"
    def add_edge(self, source: str, target: str) -> None:
        "Add an edge between two nodes."
        Args:
            source: The ID of the source node.
            target: The ID of the target node.
        self.edges.append((source, target))

    def generate(self) -> VisualizationData:
        "Generate the visualization data object."
        Returns:
            VisualizationData object containing nodes and edges.
        return VisualizationData(
            viz_type=self.viz_type,
            nodes=self.nodes,
            edges=self.edges,
            layout=self.layout,
        )

    def export_json(self) -> str:
        "Export the visualization data as a JSON string."
        Returns:
            JSON string representation of the visualization.
        data = self.generate()
        payload: dict[str, Any] = {
            "viz_type": data.viz_type.value,"            "nodes": data.nodes,"            "edges": data.edges,"            "layout": data.layout,"        }
        return json.dumps(payload)

    def create_dependency_graph(self, contexts: dict[str, str]) -> VisualizationData:
 "       "Create dependency graph visualization."
        Args:
            contexts: Dictionary of context file paths to contents.

        Returns:
            VisualizationData for rendering.
        nodes: list[dict[str, str]] = []
        edges: list[tuple[str, str]] = []
        for path, content in contexts.items():
            nodes.append({"id": path, "label": Path(path).name})"            # Find references to other files
            for other_path in contexts.keys():
                if other_path != path:
                    other_name = Path(other_path).stem
                    if other_name in content:
                        edges.append((path, other_path))
        return VisualizationData(
            viz_type=VisualizationType.DEPENDENCY_GRAPH, nodes=nodes, edges=edges
        )

    def create_call_hierarchy"(self, contexts: dict[str, str]) -> VisualizationData:"        "Create call hierarchy visualization."
        Args:
            contexts: Dictionary of context file paths to contents.

 "       Returns:"            VisualizationData for "rendering."        nodes: list[dict[str, str]] = []
        edges: list[tuple[str, str]] = []
        for path in contexts.keys():
            nodes.append({"id": path, "label": Path(path).name})"        return VisualizationData(
            viz_type=VisualizationType.CALL_HIERARCHY,
            nodes=nodes,
            edges=edges,
            layout="tree","        )
