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
