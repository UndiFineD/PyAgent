# Engine

**File**: `src\infrastructure\reasoning\Engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 22 imports  
**Lines**: 170  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for Engine.

## Classes (1)

### `ReasoningEngine`

Unified reasoning and tool call extraction engine.

**Methods** (8):
- `__init__(self, reasoning_format, tool_format, enable_thinking, cache_thoughts, max_cached_thoughts)`
- `parse(self, text)`
- `parse_streaming(self, token_stream)`
- `detect_format(self, text)`
- `score_reasoning(self, block)`
- `visualize_reasoning(self, result)`
- `get_stats(self)`
- `reset(self)`

## Functions (2)

### `create_reasoning_engine(model_name, enable_thinking, tool_format)`

### `create_tool_parser(format_type, strict)`

## Dependencies

**Imports** (22):
- `DataClasses.ParseResult`
- `DataClasses.ThinkingBlock`
- `DataClasses.ToolCall`
- `Enums.ParseState`
- `Enums.ReasoningFormat`
- `Enums.ToolCallFormat`
- `Implementations.DeepSeekReasoningParser`
- `Implementations.GenericReasoningParser`
- `Implementations.HermesToolParser`
- `Implementations.OpenAIToolParser`
- `Implementations.QwenReasoningParser`
- `Parsers.ReasoningParser`
- `Parsers.ToolParser`
- `collections.deque`
- `json`
- ... and 7 more

---
*Auto-generated documentation*
