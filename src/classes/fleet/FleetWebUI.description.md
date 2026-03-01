# FleetWebUI

**File**: `src\classes\fleet\FleetWebUI.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 145  
**Complexity**: 10 (moderate)

## Overview

Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.

## Classes (1)

### `FleetWebUI`

Provides backend support for the Fleet visualization dashboard.

**Methods** (10):
- `__init__(self, fleet_manager)`
- `register_generative_component(self, name, description, props_schema)`
- `suggest_ui_components(self, task_result)`
- `get_fleet_topology(self)`
- `generate_workflow_graph(self, workflow_state)`
- `get_metrics_snapshot(self)`
- `list_workspace_files(self, sub_path)`
- `_get_preview(self, file_path)`
- `get_workflow_designer_state(self)`
- `get_multi_fleet_manager(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
