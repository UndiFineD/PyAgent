# SelfHealingEngineCore

**File**: `src\classes\orchestration\SelfHealingEngineCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 33  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SelfHealingEngineCore.

## Classes (1)

### `SelfHealingEngineCore`

Pure logic for self-healing analysis.
Decides what kind of fix is needed based on the traceback.

**Methods** (2):
- `analyze_failure(self, agent_name, tool_name, error_msg, tb)`
- `format_healing_report(self, history)`

## Dependencies

**Imports** (4):
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
