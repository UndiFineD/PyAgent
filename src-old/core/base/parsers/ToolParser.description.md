# ToolParser

**File**: `src\core\base\parsers\ToolParser.py`  
**Type**: Python Module  
**Summary**: 7 classes, 2 functions, 14 imports  
**Lines**: 511  
**Complexity**: 19 (moderate)

## Overview

ToolParser - Extensible tool call parsing framework.

Inspired by vLLM's ToolParser pattern for extracting tool calls from
LLM outputs with support for streaming and lazy registration.

Phase 24: Advanced Observability & Parsing

## Classes (7)

### `ToolCall`

Represents a single tool/function call.

**Methods** (1):
- `to_dict(self)`

### `ExtractedToolCalls`

Result of tool call extraction.

**Methods** (1):
- `has_tool_calls(self)`

### `StreamingToolCallDelta`

Delta update for streaming tool call extraction.

### `ToolParser`

**Inherits from**: ABC

Abstract base class for tool call parsers.

Implementations should handle extracting tool calls from
model outputs in both complete and streaming modes.

**Methods** (5):
- `__init__(self, tokenizer)`
- `vocab(self)`
- `extract_tool_calls(self, model_output, tools)`
- `extract_tool_calls_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids)`
- `reset(self)`

### `JSONToolParser`

**Inherits from**: ToolParser

Parser for JSON-formatted tool calls.

Handles outputs like:
[{"name": "function_name", "arguments": {"arg1": "value1"}}]

**Methods** (3):
- `__init__(self, tokenizer, tool_call_start, tool_call_end)`
- `extract_tool_calls(self, model_output, tools)`
- `extract_tool_calls_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids)`

### `XMLToolParser`

**Inherits from**: ToolParser

Parser for XML-formatted tool calls.

Handles outputs like:
<tool_call>
    <name>function_name</name>
    <arguments>{"arg1": "value1"}</arguments>
</tool_call>

**Methods** (2):
- `extract_tool_calls(self, model_output, tools)`
- `extract_tool_calls_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids)`

### `ToolParserManager`

Central registry for ToolParser implementations.

Supports both eager and lazy registration.

**Methods** (5):
- `register(cls, name, parser_cls)`
- `register_lazy(cls, name, module, class_name)`
- `get(cls, name)`
- `create(cls, name)`
- `list_parsers(cls)`

## Functions (2)

### `tool_parser(name)`

Decorator for registering a ToolParser.

Usage:
    @tool_parser("my_parser")
    class MyParser(ToolParser): ...

### `extract_tool_calls(model_output, parser_name, tools)`

Convenience function for extracting tool calls.

Args:
    model_output: Model-generated text
    parser_name: Name of parser to use
    tools: Optional tool definitions
    **parser_kwargs: Additional parser arguments
    
Returns:
    ExtractedToolCalls result

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.abc.Callable`
- `collections.abc.Sequence`
- `dataclasses.dataclass`
- `dataclasses.field`
- `functools.cached_property`
- `importlib`
- `json`
- `partial_json_parser`
- `re`
- `typing.Any`
- `typing.TypeVar`

---
*Auto-generated documentation*
