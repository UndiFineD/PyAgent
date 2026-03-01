# FleetTaskMixin

**File**: `src\infrastructure\fleet\mixins\FleetTaskMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 75  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for FleetTaskMixin.

## Classes (1)

### `FleetTaskMixin`

Mixin for task execution, preemption, and consensus management in FleetManager.

**Methods** (3):
- `preempt_lower_priority_tasks(self, new_priority)`
- `resume_tasks(self)`
- `execute_with_consensus(self, task, primary_agent, secondary_agents)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.models.AgentPriority`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
