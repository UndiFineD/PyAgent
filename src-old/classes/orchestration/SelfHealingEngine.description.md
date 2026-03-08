# SelfHealingEngine

**File**: `src\classes\orchestration\SelfHealingEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 40  
**Complexity**: 3 (simple)

## Overview

Engine for automated self-repair of agent tools and modules.
Detects runtime errors and orchestrates CoderAgents to apply fixes.

## Classes (1)

### `SelfHealingEngine`

Monitors tool execution and attempts automatic fixes for crashes.
Shell for SelfHealingEngineCore.

**Methods** (3):
- `__init__(self, workspace_root)`
- `handle_failure(self, agent, tool_name, error, context)`
- `get_healing_stats(self)`

## Dependencies

**Imports** (9):
- `SelfHealingEngineCore.SelfHealingEngineCore`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
