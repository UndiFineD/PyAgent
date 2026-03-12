#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/utils/MemoryCore.description.md

# MemoryCore

**File**: `src\logic\agents\cognitive\context\utils\MemoryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 67  
**Complexity**: 5 (moderate)

## Overview

MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.

## Classes (1)

### `MemoryCore`

Class MemoryCore implementation.

**Methods** (5):
- `__init__(self, baseline_utility)`
- `create_episode(self, agent_name, task, outcome, success, metadata)`
- `format_for_indexing(self, episode)`
- `calculate_new_utility(self, old_score, increment)`
- `filter_relevant_memories(self, memories, min_utility)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `datetime.datetime`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/utils/MemoryCore.improvements.md

# Improvements for MemoryCore

**File**: `src\logic\agents\cognitive\context\utils\MemoryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 67 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: MemoryCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryCore_test.py` with pytest tests

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
MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.
"""

from src.core.base.version import VERSION
from typing import Dict, List, Any, Optional
from datetime import datetime

__version__ = VERSION


class MemoryCore:
    def __init__(self, baseline_utility: float = 0.5) -> None:
        self.baseline_utility = baseline_utility

    def create_episode(
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Pure logic to construct an episode and calculate utility."""
        timestamp = datetime.now().isoformat()
        utility_score = self.baseline_utility

        if success:
            utility_score += 0.2
        else:
            utility_score -= 0.3

        return {
            "timestamp": timestamp,
            "agent": agent_name,
            "task": task,
            "outcome": outcome,
            "success": success,
            "utility_score": max(0.0, min(1.0, utility_score)),
            "metadata": metadata or {},
        }

    def format_for_indexing(self, episode: dict[str, Any]) -> str:
        """Standardized string representation for vector databases."""
        return (
            f"Agent: {episode['agent']}\n"
            f"Task: {episode['task']}\n"
            f"Outcome: {episode['outcome']}\n"
            f"Success: {episode['success']}"
        )

    def calculate_new_utility(self, old_score: float, increment: float) -> float:
        """Logic for utility score decay/boost."""
        return max(0.0, min(1.0, old_score + increment))

    def filter_relevant_memories(
        self, memories: list[dict[str, Any]], min_utility: float = 0.3
    ) -> list[dict[str, Any]]:
        """Filters memories by utility threshold."""
        return [m for m in memories if m.get("utility_score", 0.0) >= min_utility]
