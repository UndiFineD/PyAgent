# NLQueryResult

**File**: `src\classes\context\NLQueryResult.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `NLQueryResult`

Result from natural language query.

Attributes:
    query: Original query string.
    answer: Generated answer.
    relevant_contexts: List of relevant context files.
    confidence: Confidence score (0 - 1).

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
