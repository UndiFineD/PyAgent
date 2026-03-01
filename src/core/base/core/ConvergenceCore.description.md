# ConvergenceCore

**File**: `src\core\base\core\ConvergenceCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 52  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ConvergenceCore.

## Classes (1)

### `ConvergenceCore`

ConvergenceCore handles the 'Full Fleet Sync' and health verification logic.
It identifies if all registered agents are passing health checks and generates summaries.

**Methods** (3):
- `__init__(self, workspace_root)`
- `verify_fleet_health(self, agent_reports)`
- `generate_strategic_summary(self, phase_history)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
