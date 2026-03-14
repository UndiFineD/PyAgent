#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/SpecToolAgent.description.md

# SpecToolAgent

**File**: `src\classes\specialized\SpecToolAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 168  
**Complexity**: 8 (moderate)

## Overview

Agent specializing in generating tools and code from specifications (OpenAPI, JSON Schema, MCP).

## Classes (1)

### `SpecToolAgent`

**Inherits from**: BaseAgent

Generates Python tool wrappers from specifications and manages OpenSpec SDD workflows.

**Methods** (8):
- `__init__(self, file_path)`
- `generate_sdd_spec(self, feature_name, details)`
- `confirm_proceed(self, confirmation)`
- `init_openspec(self)`
- `create_proposal(self, name, intent)`
- `archive_change(self, name)`
- `generate_tool_from_spec(self, spec_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/SpecToolAgent.improvements.md

# Improvements for SpecToolAgent

**File**: `src\classes\specialized\SpecToolAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 168 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SpecToolAgent_test.py` with pytest tests

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


r"""Agent specializing in generating tools and code from specifications (OpenAPI, JSON Schema, MCP)."""
