# DataClasses

**File**: `src\infrastructure\reasoning\DataClasses.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 10 imports  
**Lines**: 85  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for DataClasses.

## Classes (5)

### `ReasoningToken`

A single token with reasoning metadata.

### `ThinkingBlock`

A complete thinking/reasoning block.

**Methods** (2):
- `__len__(self)`
- `get_steps(self, delimiter)`

### `ToolCall`

A parsed tool/function call.

**Methods** (1):
- `to_dict(self)`

### `ToolCallResult`

Result from tool execution.

### `ParseResult`

Result of parsing a generation stream.

**Methods** (3):
- `has_thinking(self)`
- `has_tool_calls(self)`
- `total_thinking_length(self)`

## Dependencies

**Imports** (10):
- `Enums.ReasoningFormat`
- `Enums.ToolCallFormat`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
