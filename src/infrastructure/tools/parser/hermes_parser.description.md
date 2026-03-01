# hermes_parser

**File**: `src\infrastructure\tools\parser\hermes_parser.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 116  
**Complexity**: 3 (simple)

## Overview

Hermes/NousResearch tool call parser.

## Classes (1)

### `HermesToolParser`

**Inherits from**: ToolParser

Hermes/NousResearch tool call parser.

Format:
<tool_call>
{"name": "...", "arguments": {...}}
</tool_call>

**Methods** (3):
- `parser_type(self)`
- `parse(self, text)`
- `parse_streaming(self, delta, state)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `base.StreamingToolState`
- `base.ToolCall`
- `base.ToolParseResult`
- `base.ToolParser`
- `base.ToolParserType`
- `json`
- `re`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
