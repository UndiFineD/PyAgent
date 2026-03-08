# UIArchitectAgent

**File**: `src\classes\specialized\UIArchitectAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 83  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for UIArchitectAgent.

## Classes (1)

### `UIArchitectAgent`

**Inherits from**: BaseAgent

Phase 54: UI Architect Agent.
Designs and generates dynamic UI layouts for the Fleet Dashboard.
Uses the 'Tambo' pattern for generative UI.

**Methods** (3):
- `__init__(self, path)`
- `design_dashboard_layout(self, active_workflow, agent_list)`
- `generate_ui_manifest(self, task_context)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
