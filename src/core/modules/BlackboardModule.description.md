# BlackboardModule

**File**: `src\core\modules\BlackboardModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 71  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for BlackboardModule.

## Classes (1)

### `BlackboardModule`

**Inherits from**: BaseModule

Consolidated core module for Blackboard operations.
Migrated from BlackboardCore.

**Methods** (7):
- `__init__(self, config)`
- `initialize(self)`
- `execute(self, action)`
- `process_post(self, key, value, agent_name)`
- `get_value(self, key)`
- `get_all_keys(self)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
