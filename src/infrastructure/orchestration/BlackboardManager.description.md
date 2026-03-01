# BlackboardManager

**File**: `src\infrastructure\orchestration\BlackboardManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 46  
**Complexity**: 4 (simple)

## Overview

Shared central memory for opportunistic agent collaboration (Blackboard Pattern).

## Classes (1)

### `BlackboardManager`

Central repository for agents to post findings and look for data.
Shell for BlackboardCore.

**Methods** (4):
- `__init__(self)`
- `post(self, key, value, agent_name)`
- `get(self, key)`
- `list_keys(self)`

## Dependencies

**Imports** (6):
- `BlackboardCore.BlackboardCore`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
