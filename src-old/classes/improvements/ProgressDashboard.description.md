# ProgressDashboard

**File**: `src\classes\improvements\ProgressDashboard.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 164  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `ProgressDashboard`

Generates progress reports and dashboards for improvements.

Tracks completion rates, velocity, and generates burndown data.

Attributes:
    reports: List of generated reports.

**Methods** (7):
- `__init__(self)`
- `generate_report(self, improvements)`
- `_calculate_velocity(self)`
- `generate_burndown(self, improvements)`
- `get_completion_rate(self, improvements)`
- `generate_bmad_strategic_grid(self, root_path)`
- `export_dashboard(self, improvements)`

## Dependencies

**Imports** (9):
- `Improvement.Improvement`
- `ImprovementStatus.ImprovementStatus`
- `ProgressReport.ProgressReport`
- `__future__.annotations`
- `datetime.datetime`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
