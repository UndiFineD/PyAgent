# RefactoringSuggestion

**File**: `src\classes\context\RefactoringSuggestion.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `RefactoringSuggestion`

Context-based refactoring suggestion.

Attributes:
    suggestion_type: Type of refactoring.
    description: What to refactor.
    affected_files: Files affected by refactoring.
    estimated_impact: Impact assessment.

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
