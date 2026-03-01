# Parsing

**File**: `src\infrastructure\openai_api\responses\Parsing.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 13 imports  
**Lines**: 52  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for Parsing.

## Classes (1)

### `ConversationBuilder`

Build conversation messages from Responses API format.

**Methods** (2):
- `from_input(input_text, instructions, messages)`
- `append_response(messages, response)`

## Functions (2)

### `parse_response_request(data)`

Parse API request to ResponseConfig.

### `_try_rust_parse_response(data)`

Try Rust-accelerated response parsing.

## Dependencies

**Imports** (13):
- `Enums.ResponseType`
- `Enums.RoleType`
- `Enums.ToolType`
- `Models.Message`
- `Models.Response`
- `Models.ResponseConfig`
- `Models.ToolCallContent`
- `Models.ToolDefinition`
- `rust_core.parse_response_json_rust`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
