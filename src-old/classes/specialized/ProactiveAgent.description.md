# ProactiveAgent

**File**: `src\classes\specialized\ProactiveAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 59  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in proactive task management and recurring workflows (Sentient pattern).

## Classes (1)

### `ProactiveAgent`

**Inherits from**: BaseAgent

Manages recurring, triggered, and scheduled tasks proactively.

**Methods** (5):
- `__init__(self, file_path)`
- `schedule_task(self, task, cron_or_delay)`
- `scan_for_triggers(self, environment_state)`
- `get_habit_recommendation(self, user_history)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
