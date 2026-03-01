# json_parser

**File**: `src\infrastructure\tools\parser\json_parser.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 168  
**Complexity**: 6 (moderate)

## Overview

Generic JSON tool call parser.

## Classes (1)

### `JsonToolParser`

**Inherits from**: ToolParser

Generic JSON tool call parser.

Expects format:
{"name": "function_name", "arguments": {...}}
or
{"function": {"name": "...", "arguments": {...}}}

**Methods** (6):
- `parser_type(self)`
- `parse(self, text)`
- `_parse_json_object(self, data, index)`
- `_extract_content(self, text, json_matches)`
- `parse_streaming(self, delta, state)`
- `_extract_last_json(self, text)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `base.StreamingToolState`
- `base.ToolCall`
- `base.ToolParseResult`
- `base.ToolParser`
- `base.ToolParserType`
- `base.extract_json_from_text`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
