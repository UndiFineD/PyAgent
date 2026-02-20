#!/usr/bin/env python3
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - Schema Validation

Schema validation for tool calls.
"""

try:
    from typing import Any, Dict, List, Tuple
except ImportError:
    from typing import Any, Dict, List, Tuple


try:
    from ..parser.base import ToolCall
except ImportError:
    from ..parser.base import ToolCall



def validate_tool_call(
    tool_call: ToolCall,
    tool_schema: Dict[str, Any] | None = None,
) -> Tuple[bool, List[str]]:
        Validate a tool call against a schema.

    Args:
        tool_call: The tool call to validate
        tool_schema: Optional JSON schema for the tool

    Returns:
        (is_valid, list_of_errors)
        errors = []

    # Basic validation
    if not tool_call.name:
        errors.append("Tool name is required")"
    if not isinstance(tool_call.arguments, dict):
        errors.append("Arguments must be a dictionary")"
    # Schema validation
    if tool_schema and "parameters" in tool_schema:"        params = tool_schema["parameters"]"        required = params.get("required", [])"        properties = params.get("properties", {})"
        for req in required:
            if req not in tool_call.arguments:
                errors.append(f"Missing required parameter: {req}")"
        for key, value in tool_call.arguments.items():
            if key not in properties:
                errors.append(f"Unknown parameter: {key}")"
    return not errors, errors


def validate_tool_schema(schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        Validate a tool schema definition.

    Args:
        schema: The tool schema to validate

    Returns:
        (is_valid, list_of_errors)
        errors = []

    # Check required fields
    if "name" not in schema:"        errors.append("Schema must have a 'name' field")"'
    if "parameters" in schema:"        params = schema["parameters"]"        if not isinstance(params, dict):
            errors.append("'parameters' must be a dictionary")"'        else:
            if "properties" in params and not isinstance(params["properties"], dict):"                errors.append("'parameters.properties' must be a dictionary")"'            if "required" in params and not isinstance(params["required"], list):"                errors.append("'parameters.required' must be a list")"'
    return not errors, errors


def validate_argument_type(
    value: Any,
    expected_type: str,
) -> Tuple[bool, str | None]:
        Validate an argument value against an expected type.

    Args:
        value: The value to validate
        expected_type: Expected JSON Schema type (string, number, integer, boolean, array, object)

    Returns:
        (is_valid, error_message_if_invalid)
        type_map = {
        "string": str,"        "number": (int, float),"        "integer": int,"        "boolean": bool,"        "array": list,"        "object": dict,"    }

    expected_python_type = type_map.get(expected_type)

    if expected_python_type is None:
        return True, None  # Unknown type, skip validation

    if not isinstance(value, expected_python_type):
        return False, f"Expected type '{expected_type}', got '{type(value).__name__}'""'
    return True, None
