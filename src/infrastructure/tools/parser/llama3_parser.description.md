# llama3_parser

**File**: `src\infrastructure\tools\parser\llama3_parser.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 220  
**Complexity**: 7 (moderate)

## Overview

Llama 3 tool call parser.

## Classes (1)

### `Llama3ToolParser`

**Inherits from**: ToolParser

Llama 3 tool call parser.

Format:
<|python_tag|>function_name(arg1=value1, arg2=value2)
or
{"name": "...", "parameters": {...}}

**Methods** (7):
- `parser_type(self)`
- `parse(self, text)`
- `_parse_pythonic_call(self, text, index)`
- `_parse_kwargs(self, args_str)`
- `_split_args(self, args_str)`
- `_parse_value(self, value)`
- `parse_streaming(self, delta, state)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base.StreamingToolState`
- `base.ToolCall`
- `base.ToolParseResult`
- `base.ToolParser`
- `base.ToolParserType`
- `json`
- `json_parser.JsonToolParser`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
