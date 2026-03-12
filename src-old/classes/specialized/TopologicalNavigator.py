#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/TopologicalNavigator.description.md

# TopologicalNavigator

**File**: `src\classes\specialized\TopologicalNavigator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 49  
**Complexity**: 1 (simple)

## Overview

Agent specializing in Topological Context Navigation.
Builds a semantic map of the codebase for graph-based dependency exploration.

## Classes (1)

### `TopologicalNavigator`

**Inherits from**: BaseAgent, MapBuilderMixin, GraphAnalysisMixin, FederationMixin

Tier 2 (Cognitive Logic) - Topological Navigator: Maps code relationships 
and determines the impact of changes using graph-based dependency analysis.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `mixins.FederationMixin.FederationMixin`
- `mixins.GraphAnalysisMixin.GraphAnalysisMixin`
- `mixins.MapBuilderMixin.MapBuilderMixin`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/TopologicalNavigator.improvements.md

# Improvements for TopologicalNavigator

**File**: `src\classes\specialized\TopologicalNavigator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TopologicalNavigator_test.py` with pytest tests

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


"""Agent specializing in Topological Context Navigation.
Builds a semantic map of the codebase for graph-based dependency exploration.
"""

from src.core.base.Version import VERSION
import os
from pathlib import Path
from .mixins.MapBuilderMixin import MapBuilderMixin
from .mixins.GraphAnalysisMixin import GraphAnalysisMixin
from .mixins.FederationMixin import FederationMixin
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION


class TopologicalNavigator(
    BaseAgent, MapBuilderMixin, GraphAnalysisMixin, FederationMixin
):
    """
    Tier 2 (Cognitive Logic) - Topological Navigator: Maps code relationships
    and determines the impact of changes using graph-based dependency analysis.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.graph: dict[str, set[str]] = {}
        self.reverse_graph: dict[str, set[str]] = {}
        self.root_dir = Path(os.getcwd())
        self._system_prompt = (
            "You are the Topological Context Navigator. "
            "You map relationships between code entities (classes, functions, modules) "
            "to determine the impact of changes across the codebase."
        )

    # Logic delegated to mixins
