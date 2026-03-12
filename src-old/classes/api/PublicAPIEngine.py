#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/api/PublicAPIEngine.description.md

# PublicAPIEngine

**File**: `src\classes\api\PublicAPIEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Public API Engine for PyAgent.
Generates OpenAPI/Swagger specs and handles external tool integration.

## Classes (1)

### `PublicAPIEngine`

Manages the external interface for third-party integrations.
Shell for APICore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `generate_openapi_spec(self)`
- `register_external_tool(self, tool_spec)`

## Dependencies

**Imports** (6):
- `APICore.APICore`
- `json`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/api/PublicAPIEngine.improvements.md

# Improvements for PublicAPIEngine

**File**: `src\classes\api\PublicAPIEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 41 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PublicAPIEngine_test.py` with pytest tests

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

"""Public API Engine for PyAgent.
Generates OpenAPI/Swagger specs and handles external tool integration.
"""

import json
import logging
from typing import Dict, List, Any
from .APICore import APICore


class PublicAPIEngine:
    """
    Manages the external interface for third-party integrations.
    Shell for APICore.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.core = APICore()

    def generate_openapi_spec(self) -> str:
        """Generates a dynamic OpenAPI 3.0 specification based on registered tools."""
        # Standardize tool data for core
        raw_tools = []
        if hasattr(self.fleet, "registry"):
            # This depends on how tools are stored, assuming a list of objects with .name
            tools = self.fleet.registry.list_tools()
            for t in tools:
                raw_tools.append(
                    {"name": t.name, "parameters": getattr(t, "parameters", None)}
                )

        return self.core.build_openapi_json(raw_tools)

    def register_external_tool(self, tool_spec: Dict[str, Any]) -> str:
        """Registers a tool from an external OpenAPI definition."""
        if not self.core.validate_tool_contract(tool_spec):
            return "Error: Invalid tool specification."

        name = tool_spec.get("name")
        logging.info(f"API-ENGINE: Importing external tool '{name}'")
        return f"Successfully registered external tool '{name}' into fleet registry."
