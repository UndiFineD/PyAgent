#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/HierarchicalMemoryAgent.description.md

# HierarchicalMemoryAgent

**File**: `src\logic\agents\cognitive\HierarchicalMemoryAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 62  
**Complexity**: 1 (simple)

## Overview

Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.

## Classes (1)

### `HierarchicalMemoryAgent`

**Inherits from**: BaseAgent, MemoryStorageMixin, MemoryQueryMixin

Manages memory across multiple temporal and semantic resolutions.
Phase 290: Integrated with 3-layer system (ShortTerm, Working, LongTerm).

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `mixins.MemoryQueryMixin.MemoryQueryMixin`
- `mixins.MemoryStorageMixin.MemoryStorageMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.create_main_function`
- `src.core.base.Version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/HierarchicalMemoryAgent.improvements.md

# Improvements for HierarchicalMemoryAgent

**File**: `src\logic\agents\cognitive\HierarchicalMemoryAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HierarchicalMemoryAgent_test.py` with pytest tests

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


"""Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.
"""

from src.core.base.Version import VERSION
from pathlib import Path
from .mixins.MemoryStorageMixin import MemoryStorageMixin
from .mixins.MemoryQueryMixin import MemoryQueryMixin
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION


class HierarchicalMemoryAgent(BaseAgent, MemoryStorageMixin, MemoryQueryMixin):
    """Manages memory across multiple temporal and semantic resolutions.
    Phase 290: Integrated with 3-layer system (ShortTerm, Working, LongTerm).
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.memory_root = Path("data/logs/memory_hierarchical")
        # Phase 290: Standardized 3-layer tiers + Archival
        self.tiers = ["ShortTerm", "Working", "LongTerm", "Archival"]
        for tier in self.tiers:
            (self.memory_root / tier).mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
            "You are the Hierarchical Memory Agent. "
            "Your role is to categorize and move information between different memory tiers. "
            "ShortTerm memory: Recent raw telemetry and episodic events. "
            "Working memory: Task-specific context and scratchpad data. "
            "LongTerm memory: Distilled semantic knowledge and reusable patterns. "
            "Archival memory: Highly compressed historical logs for auditing."
        )

    # Logic delegated to mixins


if __name__ == "__main__":
    from src.core.base.BaseUtilities import create_main_function

    main = create_main_function(
        HierarchicalMemoryAgent,
        "Hierarchical Memory Agent",
        "Multi-resolution memory management",
    )
    main()
