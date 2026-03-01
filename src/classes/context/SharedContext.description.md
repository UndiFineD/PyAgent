# SharedContext

**File**: `src\classes\context\SharedContext.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 36  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `SharedContext`

Context shared with team members.

Attributes:
    context_id: Unique identifier.
    owner: Owner username.
    shared_with: List of usernames shared with.
    permission: Permission level.
    last_sync: Last synchronization timestamp.

## Dependencies

**Imports** (18):
- `SharingPermission.SharingPermission`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
