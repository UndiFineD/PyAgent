#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/api/APICore.description.md

# APICore

**File**: `src\classes\api\APICore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 75  
**Complexity**: 3 (simple)

## Overview

APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.

## Classes (1)

### `APICore`

Class APICore implementation.

**Methods** (3):
- `__init__(self, version)`
- `build_openapi_json(self, tool_definitions)`
- `validate_tool_contract(self, spec)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `src.core.base.version.SDK_VERSION`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/api/APICore.improvements.md

# Improvements for APICore

**File**: `src\classes\api\APICore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 75 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: APICore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `APICore_test.py` with pytest tests

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.
"""

from src.core.base.version import VERSION
import json
from typing import Dict, List, Any
from src.core.base.version import SDK_VERSION

__version__ = VERSION


class APICore:
    def __init__(self, version: str = SDK_VERSION) -> None:
        self.version = version

    def build_openapi_json(self, tool_definitions: list[dict[str, Any]]) -> str:
        """Constructs an OpenAPI 3.0 string from tool metadata."""
        paths = {}
        for tool in tool_definitions:
            tool_name = tool.get("name", "unknown")
            paths[f"/tools/{tool_name}"] = {
                "post": {
                    "summary": f"Execute {tool_name}",
                    "operationId": tool_name,
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": tool.get(
                                        "parameters", {"input": {"type": "string"}}
                                    ),
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "OK"}},
                }
            }

        spec = {
            "openapi": "3.0.0",
            "info": {"title": "PyAgent Fleet API", "version": self.version},
            "paths": paths,
        }
        return json.dumps(spec, indent=2)

    def validate_tool_contract(self, spec: dict[str, Any]) -> bool:
        """Checks if an external tool definition is valid."""
        return "name" in spec and ("endpoint" in spec or "implementation" in spec)
