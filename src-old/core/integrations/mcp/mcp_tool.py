# Copyright 2025.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM_CONTEXT_START

## Source: src-old/core/integrations/mcp/mcp_tool.description.md

# mcp_tool

**File**: `src\core\integrations\mcp\mcp_tool.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 8 imports  
**Lines**: 132  
**Complexity**: 3 (simple)

## Overview

MCP-based tool registration using official mcp library.
Provides register_tool decorator compatible with mcp.mcp_tool.

## Functions (3)

### `register_tool(name, description)`

Decorator to register a function as a tool using MCP format.
Compatible with mcp.mcp_tool descriptor.

Args:
    name: Optional custom tool name
    description: Optional custom description

### `_generate_mcp_schema(func)`

Generate MCP-compatible JSON schema from function signature.

### `create_mcp_server(name, version)`

Create MCP server with registered tools.

Args:
    name: Server name
    version: Server version

Returns:
    MCP server instance

## Dependencies

**Imports** (8):
- `aenv.core.tool.get_registry`
- `inspect`
- `mcp.server.fastapi.serve_app`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.get_type_hints`

---
*Auto-generated documentation*
## Source: src-old/core/integrations/mcp/mcp_tool.improvements.md

# Improvements for mcp_tool

**File**: `src\core\integrations\mcp\mcp_tool.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 132 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `mcp_tool_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
MCP-based tool registration using official mcp library.
Provides register_tool decorator compatible with mcp.mcp_tool.
"""

import inspect
from typing import Any, Callable, Dict, Optional, get_type_hints

# Delay importing mcp to avoid dependency conflicts during test loading
try:
    from mcp.server.fastapi import serve_app
except Exception:  # environment may not have compatible pydantic
    serve_app = None  # type: ignore

from aenv.core.tool import get_registry


def register_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
):
    """
    Decorator to register a function as a tool using MCP format.
    Compatible with mcp.mcp_tool descriptor.

    Args:
        name: Optional custom tool name
        description: Optional custom description
    """

    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool {tool_name}"

        # Register with global registry
        registry = get_registry()

        # Check for duplicate registration
        if tool_name in [t.name for t in registry.list_tools()]:
            raise ValueError(f"Tool '{tool_name}' already registered")

        registry.register(func, name=tool_name, description=tool_description)

        return func

    return decorator


def _generate_mcp_schema(func: Callable) -> Dict[str, Any]:
    """Generate MCP-compatible JSON schema from function signature."""
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue

        param_type = type_hints.get(param_name, str)

        # Convert Python types to JSON schema types
        type_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
            list[str]: "array",
            list[int]: "array",
            dict[str, Any]: "object",
        }

        json_type = type_mapping.get(param_type, "string")

        properties[param_name] = {
            "type": json_type,
            "description": f"Parameter {param_name}",
        }

        if param.default == inspect.Parameter.empty:
            required.append(param_name)
        else:
            properties[param_name]["default"] = param.default

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def create_mcp_server(name: str = "aenv-server", version: str = "0.1.0"):
    """
    Create MCP server with registered tools.

    Args:
        name: Server name
        version: Server version

    Returns:
        MCP server instance
    """

    registry = get_registry()

    # Create MCP server
    server = serve_app(
        name=name,
        version=version,
    )

    # Register all tools
    for tool_descriptor in registry.list_tools():
        tool_func = registry.get_tool(tool_descriptor.name)
        if tool_func:
            server.tool()(tool_func)

    return server
