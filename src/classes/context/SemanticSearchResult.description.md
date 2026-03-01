# SemanticSearchResult

**File**: `src\classes\context\SemanticSearchResult.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `SemanticSearchResult`

Result from semantic code search.

Attributes:
    file_path: Path to the matching file.
    content_snippet: Relevant code snippet.
    similarity_score: Similarity score (0 - 1).
    context_type: Type of context matched.
    line_range: Tuple of start and end line numbers.

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
