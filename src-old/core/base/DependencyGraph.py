#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/DependencyGraph.description.md

# DependencyGraph

**File**: `src\\core\base\\DependencyGraph.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 126  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `DependencyGraph`

Resolve agent dependencies for ordered execution.

Example:
    graph=DependencyGraph()
    graph.add_dependency("tests", "coder")  # tests depends on coder
    graph.add_dependency("docs", "tests")

    order=graph.resolve()  # [["coder"], ["tests"], ["docs"]]

**Methods** (5):
- `__init__(self)`
- `add_node(self, name, resources)`
- `add_dependency(self, node, depends_on)`
- `resolve(self)`
- `_refine_batch_by_resources(self, batch)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `graphlib`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/core/base/DependencyGraph.improvements.md

# Improvements for DependencyGraph

**File**: `src\\core\base\\DependencyGraph.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 126 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DependencyGraph_test.py` with pytest tests

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


r"""Auto-extracted class from agent.py"""
