# DashboardAgent

**File**: `src\classes\specialized\DashboardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 55  
**Complexity**: 3 (simple)

## Overview

Agent specializing in UI generation and Dashboard management.
Helps create Next.js or React interfaces for the fleet.

## Classes (1)

### `DashboardAgent`

**Inherits from**: BaseAgent

Generates and maintains the Fleet Dashboard UI.

**Methods** (3):
- `__init__(self, file_path)`
- `generate_component(self, name, description)`
- `update_dashboard_layout(self, active_agents)`

## Dependencies

**Imports** (9):
- `logging`
- `os`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
