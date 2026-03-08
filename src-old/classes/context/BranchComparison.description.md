# BranchComparison

**File**: `src\classes\context\BranchComparison.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 35  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `BranchComparison`

Comparison of context across branches.

Attributes:
    branch_a: First branch name.
    branch_b: Second branch name.
    files_only_in_a: Files only in branch A.
    files_only_in_b: Files only in branch B.
    modified_files: Files modified between branches.

## Dependencies

**Imports** (18):
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
- ... and 3 more

---
*Auto-generated documentation*
