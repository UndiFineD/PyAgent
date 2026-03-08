# orchestrator_work_pattern_mixin

**File**: `src\logic\agents\swarm\orchestrator_work_pattern_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 121  
**Complexity**: 5 (moderate)

## Overview

OrchestratorWorkPatternMixin: Mixin for work pattern orchestration in PyAgent.

## Classes (1)

### `OrchestratorWorkPatternMixin`

Mixin class that provides work pattern orchestration capabilities to OrchestratorAgent.

Enables the orchestrator to execute structured collaborative workflows using
predefined work patterns like PEER (Planning, Executing, Expressing, Reviewing).

**Methods** (5):
- `__init__(self)`
- `register_work_pattern(self, pattern)`
- `get_work_pattern(self, name)`
- `list_work_patterns(self)`
- `validate_work_pattern_setup(self, pattern_name)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.work_patterns.WorkPattern`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
