#!/usr/bin/env python3
"""Minimal DAG workflow core used by tests."""
try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any, Dict, List
except ImportError:
    from typing import Any, Dict, List

try:
    from collections import defaultdict, deque
except ImportError:
    from collections import defaultdict, deque



@dataclass
class WorkflowNode:
    id: str
    task_description: str
    dependencies: List[str] = field(default_factory=list)
    results: Any = None
    status: str = "pending"


class DAGWorkflowCore:
    def __init__(self) -> None:
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = defaultdict(list)

    def add_step(self, node_id: str, description: str, dependencies: List[str] | None = None) -> None:
        self.nodes[node_id] = WorkflowNode(id=node_id, task_description=description, dependencies=dependencies or [])
        for dep in (dependencies or []):
            self.edges[dep].append(node_id)

    def get_executable_nodes(self) -> List[str]:
        executable: List[str] = []
        for node_id, node in self.nodes.items():
            if node.status != "pending":
                continue
            if all(self.nodes[dep].status == "completed" for dep in node.dependencies):
                executable.append(node_id)
        return executable

    def mark_completed(self, node_id: str, results: Any = None) -> None:
        if node_id in self.nodes:
            self.nodes[node_id].status = "completed"
            self.nodes[node_id].results = results

    def is_workflow_complete(self) -> bool:
        return all(node.status == "completed" for node in self.nodes.values())

    def get_order(self) -> List[str]:
        in_degree = {u: 0 for u in self.nodes}
        for u in self.nodes:
            for v in self.edges.get(u, []):
                in_degree[v] = in_degree.get(v, 0) + 1

        q = deque([u for u, d in in_degree.items() if d == 0])
        order: List[str] = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.edges.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)

        if len(order) != len(self.nodes):
            raise ValueError("Cycle detected in the workflow graph!")
        return order


__all__ = ["WorkflowNode", "DAGWorkflowCore"]
