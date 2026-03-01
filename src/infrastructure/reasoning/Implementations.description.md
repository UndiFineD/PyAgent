# Implementations

**File**: `src\infrastructure\reasoning\Implementations.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 15 imports  
**Lines**: 353  
**Complexity**: 15 (moderate)

## Overview

Python module containing implementation for Implementations.

## Classes (5)

### `DeepSeekReasoningParser`

**Inherits from**: ReasoningParser

Parser for DeepSeek R1-style <think>...</think> blocks.

**Methods** (3):
- `__init__(self)`
- `extract_thinking(self, text)`
- `parse_streaming(self, token_stream)`

### `QwenReasoningParser`

**Inherits from**: ReasoningParser

Parser for Qwen3-style reasoning with enable_thinking flag.

**Methods** (3):
- `__init__(self, enable_thinking)`
- `extract_thinking(self, text)`
- `parse_streaming(self, token_stream)`

### `GenericReasoningParser`

**Inherits from**: ReasoningParser

Configurable parser for any reasoning format.

**Methods** (3):
- `__init__(self, start_marker, end_marker, nested)`
- `extract_thinking(self, text)`
- `parse_streaming(self, token_stream)`

### `OpenAIToolParser`

**Inherits from**: ToolParser

Class OpenAIToolParser implementation.

**Methods** (3):
- `__init__(self, strict)`
- `parse_tool_calls(self, text)`
- `parse_streaming(self, token_stream)`

### `HermesToolParser`

**Inherits from**: ToolParser

Class HermesToolParser implementation.

**Methods** (3):
- `__init__(self, strict)`
- `parse_tool_calls(self, text)`
- `parse_streaming(self, token_stream)`

## Dependencies

**Imports** (15):
- `DataClasses.ParseResult`
- `DataClasses.ThinkingBlock`
- `DataClasses.ToolCall`
- `Enums.ParseState`
- `Enums.ReasoningFormat`
- `Enums.ToolCallFormat`
- `Parsers.ReasoningParser`
- `Parsers.ToolParser`
- `json`
- `re`
- `typing.Generator`
- `typing.Iterator`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
