# StrategicPlanningAgent

**File**: `src\classes\specialized\StrategicPlanningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 99  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for StrategicPlanningAgent.

## Classes (1)

### `StrategicPlanningAgent`

**Inherits from**: BaseAgent

Strategic Planning Agent: Handles long-term goal setting, roadmap 
prioritization, and autonomous project management for the fleet.

**Methods** (7):
- `__init__(self, workspace_path)`
- `set_long_term_goal(self, goal_description, target_date)`
- `add_milestone_to_goal(self, goal_id, milestone_description)`
- `generate_roadmap(self)`
- `_calculate_completion(self, goal)`
- `mark_milestone_complete(self, goal_id, milestone_description)`
- `get_strategic_summary(self)`

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
