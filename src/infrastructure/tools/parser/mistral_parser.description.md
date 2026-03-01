# mistral_parser

**File**: `src\infrastructure\tools\parser\mistral_parser.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 119  
**Complexity**: 3 (simple)

## Overview

Mistral AI tool call parser.

## Classes (1)

### `MistralToolParser`

**Inherits from**: ToolParser

Mistral AI tool call parser.

Format:
[TOOL_CALLS] [{"name": "...", "arguments": {...}}]

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
