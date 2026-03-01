# AndroidAgent

**File**: `src\classes\specialized\AndroidAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 113  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for AndroidAgent.

## Classes (1)

### `AndroidAgent`

**Inherits from**: BaseAgent

Automates Android devices using the 'Action-State' pattern (Accessibility Tree).
95% cheaper and 5x faster than vision-based mobile automation.

**Methods** (5):
- `__init__(self, file_path)`
- `_record(self, action, details)`
- `dump_accessibility_tree(self)`
- `execute_mobile_action(self, action_type, params)`
- `run_mobile_workflow(self, goal)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `src.logic.agents.development.core.AndroidCore.AndroidCore`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
