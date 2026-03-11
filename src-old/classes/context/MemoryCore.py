#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/context/MemoryCore.description.md

# MemoryCore

**File**: `src\classes\context\MemoryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 50  
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

**Imports** (5):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/MemoryCore.improvements.md

# Improvements for MemoryCore

**File**: `src\classes\context\MemoryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: MemoryCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryCore_test.py` with pytest tests

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

"""
MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class MemoryCore:
    def __init__(self, baseline_utility: float = 0.5) -> None:
        self.baseline_utility = baseline_utility

    def create_episode(
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
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

    def format_for_indexing(self, episode: Dict[str, Any]) -> str:
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
        self, memories: List[Dict[str, Any]], min_utility: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Filters memories by utility threshold."""
        return [m for m in memories if m.get("utility_score", 0.0) >= min_utility]
