# ToolCore

**File**: `src\classes\orchestration\ToolCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 52  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ToolCore.

## Classes (2)

### `ToolMetadata`

**Inherits from**: BaseModel

Metadata for a registered tool.

### `ToolCore`

Pure logic for tool registration and invocation.
Handles parameter introspection and argument filtering.

**Methods** (2):
- `extract_metadata(self, owner_name, func, category, priority)`
- `filter_arguments(self, func, args_dict)`

## Dependencies

**Imports** (7):
- `inspect`
- `pydantic.BaseModel`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
