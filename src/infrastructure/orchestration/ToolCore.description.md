# ToolCore

**File**: `src\infrastructure\orchestration\ToolCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 138  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ToolCore.

## Classes (2)

### `ToolMetadata`

**Inherits from**: BaseModel

Metadata for a registered tool.

### `ToolCore`

Pure logic for tool registration and invocation.
Handles parameter introspection and argument filtering.

**Methods** (5):
- `extract_metadata(self, owner_name, func, category, priority)`
- `filter_arguments(self, func, args_dict)`
- `score_tool_relevance(self, metadata, query)`
- `update_reliability(self, metadata, success, weight)`
- `selection_tournament(self, candidates, tournament_size)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `collections.abc.Callable`
- `inspect`
- `pydantic.BaseModel`
- `random`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
