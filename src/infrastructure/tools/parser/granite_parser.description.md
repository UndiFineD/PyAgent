# granite_parser

**File**: `src\infrastructure\tools\parser\granite_parser.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 107  
**Complexity**: 3 (simple)

## Overview

IBM Granite tool call parser.

## Classes (1)

### `GraniteToolParser`

**Inherits from**: ToolParser

IBM Granite tool call parser.

Format:
<|tool_call|>
{"name": "...", "arguments": {...}}
<|end_of_text|>

**Methods** (3):
- `parser_type(self)`
- `parse(self, text)`
- `parse_streaming(self, delta, state)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `base.StreamingToolState`
- `base.ToolCall`
- `base.ToolParseResult`
- `base.ToolParser`
- `base.ToolParserType`
- `json`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
