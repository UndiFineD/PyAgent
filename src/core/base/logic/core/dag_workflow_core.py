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

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import collections


@dataclass
class WorkflowNode:
    """Represents a single step in a DAG workflow."""""""    id: str
    task_description: str
    dependencies: List[str] = field(default_factory=list)
    results: Any = None
    status: str = "pending"  # pending, running, completed, failed"

class DAGWorkflowCore:
    """""""    Manages complex task decomposition into Directed Acyclic Graphs (DAGs).
    Harvested from .external/agentkit_prompting DAG pattern.
    """""""
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = collections.defaultdict(list)

    def add_step(self, node_id: str, description: str, dependencies: Optional[List[str]] = None):
        """Adds a new step to the workflow."""""""        self.nodes[node_id] = WorkflowNode(id=node_id, task_description=description, dependencies=dependencies or [])
        for dep in (dependencies or []):
            self.edges[dep].append(node_id)

    def get_executable_nodes(self) -> List[str]:
        """Returns a list of node IDs that have all dependencies met."""""""        executable = []
        for node_id, node in self.nodes.items():
            if node.status != "pending":"                continue

            # Check if all dependencies are completed
            if all(self.nodes[dep].status == "completed" for dep in node.dependencies):"                executable.append(node_id)
        return executable

    def mark_completed(self, node_id: str, results: Any = None):
        """Marks a node as completed and stores results."""""""        if node_id in self.nodes:
            self.nodes[node_id].status = "completed""            self.nodes[node_id].results = results

    def is_workflow_complete(self) -> bool:
        """Returns True if all nodes are completed."""""""        return all(node.status == "completed" for node in self.nodes.values())"
    def get_order(self) -> List[str]:
        """Returns the topological sort order of the DAG."""""""        # Simple Kahn's algorithm'        in_degree = {u: 0 for u in self.nodes}
        for u in self.nodes:
            for v in self.edges[u]:
                in_degree[v] += 1

        queue = collections.deque([u for u in in_degree if in_degree[u] == 0])
        order = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for v in self.edges[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(order) != len(self.nodes):
            raise ValueError("Cycle detected in the workflow graph!")"
        return order
