#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/GraphContextEngine.description.md

# GraphContextEngine

**File**: `src\classes\context\GraphContextEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 126  
**Complexity**: 6 (moderate)

## Overview

Core engine for managing code relationships as a graph.

## Classes (1)

### `GraphContextEngine`

Manages an adjacency list of file and class dependencies.

**Methods** (6):
- `__init__(self, workspace_root)`
- `add_edge(self, source, target, relationship)`
- `scan_project(self, start_path)`
- `get_impact_radius(self, node, max_depth)`
- `save(self)`
- `load(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.GraphCore.GraphCore`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/classes/context/GraphContextEngine.improvements.md

# Improvements for GraphContextEngine

**File**: `src\classes\context\GraphContextEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 126 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GraphContextEngine_test.py` with pytest tests

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


r"""Core engine for managing code relationships as a graph."""
