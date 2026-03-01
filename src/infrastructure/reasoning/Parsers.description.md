# Parsers

**File**: `src\infrastructure\reasoning\Parsers.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 75  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for Parsers.

## Classes (2)

### `ReasoningParser`

**Inherits from**: ABC

Abstract base for reasoning token extraction.

**Methods** (4):
- `__init__(self, reasoning_format, start_marker, end_marker)`
- `extract_thinking(self, text)`
- `parse_streaming(self, token_stream)`
- `reset(self)`

### `ToolParser`

**Inherits from**: ABC

Abstract base for tool/function call parsing.

**Methods** (5):
- `__init__(self, tool_format, strict)`
- `parse_tool_calls(self, text)`
- `parse_streaming(self, token_stream)`
- `generate_call_id(self)`
- `reset(self)`

## Dependencies

**Imports** (13):
- `DataClasses.ParseResult`
- `DataClasses.ThinkingBlock`
- `DataClasses.ToolCall`
- `Enums.ParseState`
- `Enums.ReasoningFormat`
- `Enums.ToolCallFormat`
- `abc.ABC`
- `abc.abstractmethod`
- `typing.Generator`
- `typing.Iterator`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
