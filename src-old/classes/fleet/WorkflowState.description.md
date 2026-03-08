# WorkflowState

**File**: `src\classes\fleet\WorkflowState.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 29  
**Complexity**: 3 (simple)

## Overview

Container for shared state and context between agents in a workflow.

## Classes (1)

### `WorkflowState`

Maintains context, variables, and history for a multi-agent session.

**Methods** (3):
- `set(self, key, value)`
- `get(self, key, default)`
- `add_history(self, agent, action, result)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
