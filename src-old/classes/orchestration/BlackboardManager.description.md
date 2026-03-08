# BlackboardManager

**File**: `src\classes\orchestration\BlackboardManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 30  
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

**Imports** (5):
- `BlackboardCore.BlackboardCore`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
