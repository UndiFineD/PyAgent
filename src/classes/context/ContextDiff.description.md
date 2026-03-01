# ContextDiff

**File**: `src\classes\context\ContextDiff.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 36  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextDiff`

Diff between context versions.

Attributes:
    version_from: Source version.
    version_to: Target version.
    added_sections: List of added sections.
    removed_sections: List of removed sections.
    modified_sections: List of modified section names.
    change_summary: Brief summary of changes.

## Dependencies

**Imports** (17):
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
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
