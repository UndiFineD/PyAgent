# AutoDebuggerOrchestrator

**File**: `src\classes\orchestration\AutoDebuggerOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 113  
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

**Imports** (12):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.coder.CoderAgent.CoderAgent`
- `src.classes.specialized.ImmuneSystemAgent.ImmuneSystemAgent`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
