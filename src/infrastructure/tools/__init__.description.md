# __init__

**File**: `src\infrastructure\tools\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 19 imports  
**Lines**: 82  
**Complexity**: 0 (simple)

## Overview

Tool/function call parsing framework with model-specific parsers.

Exports:
    - ToolParserType: Parser type enum
    - ToolCall: Parsed tool call
    - ToolParseResult: Parse result with validation
    - ToolParser: Base parser protocol
    - ToolParserRegistry: Parser registration
    - StreamingToolParser: Streaming extraction

Structure:
    - parser/     - Base classes and parser implementations
    - validator/  - Schema validation logic
    - registry/   - Parser registry and streaming parser

## Dependencies

**Imports** (19):
- `parser.GraniteToolParser`
- `parser.HermesToolParser`
- `parser.JsonToolParser`
- `parser.Llama3ToolParser`
- `parser.MistralToolParser`
- `parser.StreamingToolState`
- `parser.ToolCall`
- `parser.ToolCallStatus`
- `parser.ToolParameter`
- `parser.ToolParseResult`
- `parser.ToolParser`
- `parser.ToolParserType`
- `parser.extract_json_from_text`
- `registry.StreamingToolParser`
- `registry.ToolParserRegistry`
- ... and 4 more

---
*Auto-generated documentation*
