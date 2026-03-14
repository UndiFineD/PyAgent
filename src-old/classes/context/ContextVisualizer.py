#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextVisualizer.description.md

# ContextVisualizer

**File**: `src\classes\context\ContextVisualizer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 116  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextVisualizer`

Visualizes context relationships.

Creates visual representations of context dependencies and hierarchies.

Example:
    >>> visualizer=ContextVisualizer()
    >>> data=visualizer.create_dependency_graph(contexts)

**Methods** (8):
- `__init__(self, viz_type)`
- `set_type(self, viz_type)`
- `add_node(self, node_id, metadata)`
- `add_edge(self, source, target)`
- `generate(self)`
- `export_json(self)`
- `create_dependency_graph(self, contexts)`
- `create_call_hierarchy(self, contexts)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `json`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.VisualizationData.VisualizationData`
- `src.logic.agents.cognitive.context.models.VisualizationType.VisualizationType`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextVisualizer.improvements.md

# Improvements for ContextVisualizer

**File**: `src\classes\context\ContextVisualizer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextVisualizer_test.py` with pytest tests

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


r"""Auto-extracted class from agent_context.py"""
