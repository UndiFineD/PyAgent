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
LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/dag_workflow_core.description.md

# dag_workflow_core

**File**: `src\core\base\logic\core\dag_workflow_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 88  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for dag_workflow_core.

## Classes (2)

### `WorkflowNode`

Represents a single step in a DAG workflow.

### `DAGWorkflowCore`

Manages complex task decomposition into Directed Acyclic Graphs (DAGs).
Harvested from .external/agentkit_prompting DAG pattern.

**Methods** (6):
- `__init__(self)`
- `add_step(self, node_id, description, dependencies)`
- `get_executable_nodes(self)`
- `mark_completed(self, node_id, results)`
- `is_workflow_complete(self)`
- `get_order(self)`

## Dependencies

**Imports** (8):
- `collections`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/dag_workflow_core.improvements.md

# Improvements for dag_workflow_core

**File**: `src\core\base\logic\core\dag_workflow_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 88 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `dag_workflow_core_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field
import collections


@dataclass
class WorkflowNode:
    """Represents a single step in a DAG workflow."""

    id: str
    task_description: str
    dependencies: List[str] = field(default_factory=list)
    results: Any = None
    status: str = "pending"  # pending, running, completed, failed


class DAGWorkflowCore:
    """
    Manages complex task decomposition into Directed Acyclic Graphs (DAGs).
    Harvested from .external/agentkit_prompting DAG pattern.
    """

    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = collections.defaultdict(list)

    def add_step(
        self, node_id: str, description: str, dependencies: Optional[List[str]] = None
    ):
        """Adds a new step to the workflow."""
        self.nodes[node_id] = WorkflowNode(
            id=node_id, task_description=description, dependencies=dependencies or []
        )
        for dep in dependencies or []:
            self.edges[dep].append(node_id)

    def get_executable_nodes(self) -> List[str]:
        """Returns a list of node IDs that have all dependencies met."""
        executable = []
        for node_id, node in self.nodes.items():
            if node.status != "pending":
                continue

            # Check if all dependencies are completed
            if all(self.nodes[dep].status == "completed" for dep in node.dependencies):
                executable.append(node_id)
        return executable

    def mark_completed(self, node_id: str, results: Any = None):
        """Marks a node as completed and stores results."""
        if node_id in self.nodes:
            self.nodes[node_id].status = "completed"
            self.nodes[node_id].results = results

    def is_workflow_complete(self) -> bool:
        """Returns True if all nodes are completed."""
        return all(node.status == "completed" for node in self.nodes.values())

    def get_order(self) -> List[str]:
        """Returns the topological sort order of the DAG."""
        # Simple Kahn's algorithm
        in_degree = {u: 0 for u in self.nodes}
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
            raise ValueError("Cycle detected in the workflow graph!")

        return order
