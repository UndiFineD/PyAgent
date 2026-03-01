# ToolParserFramework

**File**: `src\infrastructure\tools\ToolParserFramework.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 20 imports  
**Lines**: 91  
**Complexity**: 0 (simple)

## Overview

Tool/function call parsing with model-specific parsers.

Inspired by vLLM's tool_parsers patterns, this module provides:
- Model-specific tool call parsing (Hermes, Llama3, Mistral, etc.)
- Streaming tool call extraction
- JSON schema validation
- Multi-tool support

Beyond vLLM:
- Unified parser registry
- Streaming partial JSON parsing
- Auto-detection of tool format
- Tool call validation

NOTE: This file is now a backwards-compatibility wrapper.
The actual implementations have been split into:
- parser/ - Base classes and parser implementations
- validator/ - Schema validation
- registry/ - Parser registry and streaming parser

## Dependencies

**Imports** (20):
- `__future__.annotations`
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
- ... and 5 more

---
*Auto-generated documentation*
