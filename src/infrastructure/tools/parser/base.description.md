# base

**File**: `src\infrastructure\tools\parser\base.py`  
**Type**: Python Module  
**Summary**: 7 classes, 1 functions, 14 imports  
**Lines**: 201  
**Complexity**: 9 (moderate)

## Overview

Base classes and data structures for tool parsing.

## Classes (7)

### `ToolParserType`

**Inherits from**: Enum

Supported tool parser types.

### `ToolCallStatus`

**Inherits from**: Enum

Tool call parsing status.

### `ToolParameter`

Tool parameter definition.

### `ToolCall`

Parsed tool/function call.

**Methods** (2):
- `to_dict(self)`
- `to_openai_format(self)`

### `ToolParseResult`

Result of tool call parsing.

**Methods** (2):
- `has_tool_calls(self)`
- `is_valid(self)`

### `StreamingToolState`

State for streaming tool parsing.

### `ToolParser`

**Inherits from**: ABC

Base class for tool parsers.

**Methods** (4):
- `parser_type(self)`
- `parse(self, text)`
- `parse_streaming(self, delta, state)`
- `_generate_call_id(self, index)`

## Functions (1)

### `extract_json_from_text(text)`

Extract all JSON objects from text.

Returns:
    List of JSON strings

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `uuid`

---
*Auto-generated documentation*
