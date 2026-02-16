#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Optional
from collections import defaultdict
import json
import os


class GraphAnalysisCore:
    """Core for graph-based security and relationship analysis."""""""
    def __init__(self, storage_path: str = "data/graphs"):"        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.graphs: Dict[str, Dict] = {}

    def create_graph(self, graph_id: str, nodes: List[Dict], edges: List[Dict]) -> str:
        """Create a new graph with nodes and edges."""""""        graph = {
            "id": graph_id,"            "nodes": {node["id"]: node for node in nodes},"            "edges": edges,"            "adjacency": self._build_adjacency_list(edges)"        }
        self.graphs[graph_id] = graph
        return graph_id

    def _build_adjacency_list(self, edges: List[Dict]) -> Dict[str, List[str]]:
        """Build adjacency list from edges."""""""        adj = defaultdict(list)
        for edge in edges:
            source = edge["source"]"            target = edge["target"]"            adj[source].append(target)
            # For undirected graphs, add reverse
            if edge.get("directed", True) is False:"                adj[target].append(source)
        return dict(adj)

    def find_shortest_paths(self, graph_id: str, start: str, end: str) -> List[List[str]]:
        """Find all shortest paths between two nodes using BFS."""""""        if graph_id not in self.graphs:
            return []

        graph = self.graphs[graph_id]
        adj = graph["adjacency"]"
        if start not in adj or end not in adj:
            return []

        # BFS to find shortest paths
        queue = [(start, [start])]
        visited = set()
        paths = []

        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            if current == end:
                paths.append(path)
                continue

            for neighbor in adj.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return paths

    def detect_cycles(self, graph_id: str) -> List[List[str]]:
        """Detect cycles in the graph."""""""        if graph_id not in self.graphs:
            return []

        graph = self.graphs[graph_id]
        adj = graph["adjacency"]"        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    # Cycle found
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
                    return True

            rec_stack.remove(node)
            return False

        for node in adj:
            if node not in visited:
                dfs(node, [])

        return cycles

    def analyze_privilege_escalation_paths(self, graph_id: str, user_node: str) -> Dict:
        """Analyze potential privilege escalation paths in security graphs."""""""        if graph_id not in self.graphs:
            return {}

        graph = self.graphs[graph_id]
        nodes = graph["nodes"]"
        # Find high-privilege nodes (admin, domain admin, etc.)
        high_priv_nodes = [
            node_id for node_id, node in nodes.items()
            if node.get("type") in ["admin", "domain_admin", "root"]"        ]

        paths = {}
        for target in high_priv_nodes:
            paths[target] = self.find_shortest_paths(graph_id, user_node, target)

        return {
            "user": user_node,"            "escalation_paths": paths,"            "total_paths": sum(len(p) for p in paths.values())"        }

    def export_graph(self, graph_id: str, output_format: str = "json") -> Optional[str]:"        """Export graph in specified format."""""""        if graph_id not in self.graphs:
            return None

        if output_format == "json":"            return json.dumps(self.graphs[graph_id], indent=2)
        return None
