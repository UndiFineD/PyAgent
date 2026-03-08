# MergeConflict

**File**: `src\classes\context\MergeConflict.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `MergeConflict`

Merge conflict information.

Attributes:
    section: Section with conflict.
    ours: Our version of content.
    theirs: Their version of content.
    resolution: Applied resolution.

## Dependencies

**Imports** (18):
- `ConflictResolution.ConflictResolution`
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
