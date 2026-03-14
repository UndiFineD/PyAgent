#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/tool_framework_mixin.description.md

# tool_framework_mixin

**File**: `src\\core\base\\mixins\tool_framework_mixin.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 19 imports  
**Lines**: 341  
**Complexity**: 12 (moderate)

## Overview

Tool Framework Mixin for BaseAgent.
Provides schema-based tool creation and management, inspired by Adorable's tool system.

## Classes (5)

### `ToolParameter`

Represents a tool parameter with validation.

**Methods** (1):
- `to_dict(self)`

### `ToolDefinition`

Complete definition of a tool.

**Methods** (1):
- `to_dict(self)`

### `ToolExecutionError`

**Inherits from**: Exception

Exception raised when tool execution fails.

### `ToolValidationError`

**Inherits from**: Exception

Exception raised when tool parameters are invalid.

### `ToolFrameworkMixin`

Mixin providing schema-based tool creation and management.
Inspired by Adorable's tool system with createTool() pattern.

**Methods** (10):
- `__init__(self)`
- `create_tool(self, tool_id, description, parameter_schema, category, version)`
- `get_tool_definitions(self)`
- `get_tool_definition(self, tool_id)`
- `unregister_tool(self, tool_id)`
- `get_tool_stats(self)`
- `_auto_discover_tools(self)`
- `_validate_tool_parameters(self, tool_def, parameters)`
- `_get_type_string(self, type_hint)`
- `_update_tool_stats(self, tool_id, success, error)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `inspect`
- `json`
- `logging`
- `pathlib.Path`
- `pydantic`
- `pydantic.BaseModel`
- `pydantic.Field`
- `pydantic.ValidationError`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 4 more

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/tool_framework_mixin.improvements.md

# Improvements for tool_framework_mixin

**File**: `src\\core\base\\mixins\tool_framework_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 341 lines (medium)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `tool_framework_mixin_test.py` with pytest tests

### Code Organization
- [TIP] **5 classes in one file** - Consider splitting into separate modules

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

"""
Tool Framework Mixin for BaseAgent.
Provides schema-based tool creation and management, inspired by Adorable's tool system.
"""
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, get_type_hints

try:
    import pydantic
    from pydantic import BaseModel, Field, ValidationError
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = object
    Field = lambda **kwargs: None
    ValidationError = Exception

from src.core.base.common.models.communication_models import CascadeContext


@dataclass
class ToolParameter:
    """
    """
