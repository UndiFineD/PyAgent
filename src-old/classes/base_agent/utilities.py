#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/classes/base_agent/utilities.description.md

# utilities

**File**: `src\classes\base_agent\utilities.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 18 imports  
**Lines**: 211  
**Complexity**: 3 (simple)

## Overview

Utility classes for BaseAgent framework.

## Functions (3)

### `setup_logging(verbosity_arg)`

Configure logging based on verbosity level.

### `as_tool(priority, category)`

Decorator to mark a method as a tool for the ToolRegistry.
Automatically records tool interactions to the fleet context shards for autonomous learning.
Can be used as @as_tool or @as_tool(priority=10).

### `create_main_function(agent_class, description, context_help)`

Create a main function for an agent class.

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `agent.BaseAgent`
- `argparse`
- `collections.abc.Callable`
- `functools.wraps`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.strategies.plan_executor`
- `sys`
- `time`
- `typing.Any`
- `typing.Optional`
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/utilities.improvements.md

# Improvements for utilities

**File**: `src\classes\base_agent\utilities.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 211 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `utilities_test.py` with pytest tests

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
# -*- coding: utf-8 -*-

r"""Utility classes for BaseAgent framework."""
