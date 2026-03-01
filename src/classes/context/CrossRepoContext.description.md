# CrossRepoContext

**File**: `src\classes\context\CrossRepoContext.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `CrossRepoContext`

Context from cross-repository analysis.

Attributes:
    repo_name: Name of the repository.
    repo_url: URL to the repository.
    related_files: List of related file paths.
    similarity_score: Overall similarity score.
    common_patterns: Patterns shared between repos.

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
