# schema

**File**: `src\infrastructure\tools\validator\schema.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 6 imports  
**Lines**: 115  
**Complexity**: 3 (simple)

## Overview

Schema validation for tool calls.

## Functions (3)

### `validate_tool_call(tool_call, tool_schema)`

Validate a tool call against a schema.

Args:
    tool_call: The tool call to validate
    tool_schema: Optional JSON schema for the tool

Returns:
    (is_valid, list_of_errors)

### `validate_tool_schema(schema)`

Validate a tool schema definition.

Args:
    schema: The tool schema to validate

Returns:
    (is_valid, list_of_errors)

### `validate_argument_type(value, expected_type)`

Validate an argument value against an expected type.

Args:
    value: The value to validate
    expected_type: Expected JSON Schema type (string, number, integer, boolean, array, object)

Returns:
    (is_valid, error_message_if_invalid)

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `parser.base.ToolCall`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
