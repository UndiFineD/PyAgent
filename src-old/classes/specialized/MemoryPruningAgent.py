"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/MemoryPruningAgent.description.md

# MemoryPruningAgent

**File**: `src\classes\specialized\MemoryPruningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 78  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for MemoryPruningAgent.

## Classes (1)

### `MemoryPruningAgent`

Optimizes Long-Term Memory (LTM) by ranking importance and 
pruning low-utility or stale data slices.

**Methods** (4):
- `__init__(self, workspace_path)`
- `rank_memory_importance(self, memory_entry)`
- `select_pruning_targets(self, memory_list, threshold)`
- `generate_archival_plan(self, memory_list)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/MemoryPruningAgent.improvements.md

# Improvements for MemoryPruningAgent

**File**: `src\classes\specialized\MemoryPruningAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 78 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryPruningAgent_test.py` with pytest tests

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


from src.core.base.version import VERSION
import time
from typing import Dict, List, Any

__version__ = VERSION


class MemoryPruningAgent:
    """
    Optimizes Long-Term Memory (LTM) by ranking importance and
    pruning low-utility or stale data slices.
    """

    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path

    def rank_memory_importance(self, memory_entry: dict[str, Any]) -> float:
        """
        Ranks a memory entry based on recency, frequency of access, and logical density.
        """
        score = 0.0

        # Factor 1: Recency
        age = time.time() - memory_entry.get("timestamp", 0)
        recency_penalty = min(0.5, age / (3600 * 24))  # Max penalty 0.5 for >1 day
        score += 0.5 - recency_penalty

        # Factor 2: Frequency
        access_count = memory_entry.get("access_count", 0)
        frequency_bonus = min(0.4, access_count * 0.1)
        score += frequency_bonus

        # Factor 3: Complexity/Density
        content = memory_entry.get("content", "")
        if "error" in content.lower() or "fix" in content.lower():
            score += 0.1  # Retain errors/fixes with higher priority

        return round(score, 3)

    def select_pruning_targets(
        self, memory_list: list[dict[str, Any]], threshold: float = 0.2
    ) -> list[dict[str, Any]]:
        """
        Identifies entries that fall below the utility threshold.
        """
        targets = []
        for i, entry in enumerate(memory_list):
            rank = self.rank_memory_importance(entry)
            if rank < threshold:
                targets.append({"index": i, "rank": rank, "id": entry.get("id")})
        return targets

    def generate_archival_plan(
        self, memory_list: list[dict[str, Any]]
    ) -> dict[str, list[str]]:
        """
        Decides which memories to move to 'cold' storage vs 'delete'.
        """
        plan: dict[str, list[str]] = {"cold_storage": [], "delete": []}
        for entry in memory_list:
            entry_id = entry.get("id")
            if not entry_id:
                continue
            rank = self.rank_memory_importance(entry)
            if rank < 0.1:
                plan["delete"].append(str(entry_id))
            elif rank < 0.3:
                plan["cold_storage"].append(str(entry_id))
        return plan
