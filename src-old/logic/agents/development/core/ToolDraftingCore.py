"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/core/ToolDraftingCore.description.md

# ToolDraftingCore

**File**: `src\logic\agents\development\core\ToolDraftingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 61  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ToolDraftingCore.

## Classes (2)

### `ToolDefinition`

Class ToolDefinition implementation.

### `ToolDraftingCore`

Pure logic for agents generating their own OpenAPI tools.
Handles schema drafting, parameter validation, and endpoint mapping.

**Methods** (3):
- `generate_openapi_spec(self, tools)`
- `validate_tool_name(self, name)`
- `map_to_python_stub(self, tool)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/core/ToolDraftingCore.improvements.md

# Improvements for ToolDraftingCore

**File**: `src\logic\agents\development\core\ToolDraftingCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 61 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: ToolDefinition

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ToolDraftingCore_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

import json
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    endpoint: str


class ToolDraftingCore:
    """Pure logic for agents generating their own OpenAPI tools.
    Handles schema drafting, parameter validation, and endpoint mapping.
    """

    def generate_openapi_spec(self, tools: list[ToolDefinition]) -> str:
        """Converts internal tool definitions into a valid OpenAPI 3.0 spec."""
        paths = {}
        for tool in tools:
            paths[f"/tools/{tool.name}"] = {
                "post": {
                    "summary": tool.description,
                    "operationId": tool.name,
                    "requestBody": {
                        "content": {"application/json": {"schema": tool.parameters}}
                    },
                    "responses": {"200": {"description": "Successful execution"}},
                }
            }

        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Dynamic Agent Tools", "version": "1.0.0"},
            "paths": paths,
        }
        return json.dumps(spec, indent=2)

    def validate_tool_name(self, name: str) -> bool:
        """Ensures tool names follow fleet naming conventions."""
        return name.isidentifier() and len(name) > 3

    def map_to_python_stub(self, tool: ToolDefinition) -> str:
        """Generates a Python function stub for the drafted tool."""
        params = tool.parameters.get("properties", {})
        args = ", ".join([f"{k}: Any" for k in params.keys()])

        return f"""
def {tool.name}({args}) -> Any:
    \"\"\"{tool.description}\"\"\"
    # Auto-generated stub for dynamic tool
    pass
"""
