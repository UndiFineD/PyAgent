# AutoDebuggerOrchestrator

**File**: `src\infrastructure\orchestration\AutoDebuggerOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 142  
**Complexity**: 3 (simple)

## Overview

AutoDebuggerOrchestrator for PyAgent.
Coordinates between ImmuneSystemAgent and CoderAgent to self-heal source code changes.
Implemented as part of Phase 40: Recursive Self-Debugging.

## Classes (1)

### `AutoDebuggerOrchestrator`

Orchestrates recursive self-debugging and code repair.

**Methods** (3):
- `__init__(self, workspace_root)`
- `validate_and_repair(self, file_path)`
- `run_fleet_self_audit(self)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.development.CoderAgent.CoderAgent`
- `src.logic.agents.security.ImmuneSystemAgent.ImmuneSystemAgent`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
