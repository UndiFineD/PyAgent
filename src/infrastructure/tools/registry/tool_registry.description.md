# tool_registry

**File**: `src\infrastructure\tools\registry\tool_registry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 1 functions, 19 imports  
**Lines**: 210  
**Complexity**: 13 (moderate)

## Overview

Tool parser registry for managing parser types and model mappings.

## Classes (2)

### `ToolParserRegistry`

Registry for tool parsers.

Features:
- Parser registration by type
- Auto-detection of parser type
- Model name to parser mapping

**Methods** (7):
- `__new__(cls)`
- `_init_registry(self)`
- `get_parser(self, parser_type)`
- `get_parser_for_model(self, model_name)`
- `register_parser(self, parser_type, parser_class)`
- `register_model_pattern(self, pattern, parser_type)`
- `detect_parser_type(self, text)`

### `StreamingToolParser`

High-level streaming tool parser.

Features:
- Auto-detects parser type
- Maintains streaming state
- Yields tool calls as they complete

**Methods** (5):
- `__init__(self, parser_type, model_name)`
- `feed(self, delta)`
- `finalize(self)`
- `reset(self)`
- `completed_tools(self)`

## Functions (1)

### `parse_tool_call(text, parser_type, model_name)`

Parse tool calls from text.

Args:
    text: Model output text
    parser_type: Specific parser type (auto-detected if None)
    model_name: Model name for parser selection

Returns:
    ToolParseResult with extracted tool calls

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `parser.GraniteToolParser`
- `parser.HermesToolParser`
- `parser.JsonToolParser`
- `parser.Llama3ToolParser`
- `parser.MistralToolParser`
- `parser.StreamingToolState`
- `parser.ToolCall`
- `parser.ToolParseResult`
- `parser.ToolParser`
- `parser.ToolParserType`
- `re`
- `threading`
- `typing.Dict`
- `typing.List`
- ... and 4 more

---
*Auto-generated documentation*
