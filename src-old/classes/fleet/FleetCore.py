#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/FleetCore.description.md

# FleetCore

**File**: `src\classes\fleet\FleetCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 74  
**Complexity**: 4 (simple)

## Overview

FleetCore logic for high-level fleet management.
Contains pure logic for tool scoring, capability mapping, and state transition validation.

## Classes (1)

### `FleetCore`

Pure logic core for the FleetManager.

**Methods** (4):
- `__init__(self, default_score_threshold)`
- `cached_logic_match(self, goal, tool_name, tool_owner)`
- `score_tool_candidates(self, goal, tools_metadata, provided_kwargs)`
- `validate_state_transition(self, current_state, next_state)`

## Dependencies

**Imports** (6):
- `functools.lru_cache`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/FleetCore.improvements.md

# Improvements for FleetCore

**File**: `src\classes\fleet\FleetCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 74 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FleetCore_test.py` with pytest tests

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

"""
FleetCore logic for high-level fleet management.
Contains pure logic for tool scoring, capability mapping, and state transition validation.
"""

from typing import Dict, List, Any, Optional, Tuple
from functools import lru_cache


class FleetCore:
    """Pure logic core for the FleetManager."""

    def __init__(self, default_score_threshold: int = 10) -> None:
        self.default_score_threshold: int = default_score_threshold

    @lru_cache(maxsize=128)
    def cached_logic_match(self, goal: str, tool_name: str, tool_owner: str) -> float:
        """Fast internal matching logic for core tools (Phase 107)."""
        score = 0.0
        g_low = goal.lower()
        n_low = tool_name.lower()
        o_low = tool_owner.lower()

        if g_low == n_low:
            score += 100.0
        elif g_low in n_low:
            score += 50.0

        if g_low == o_low:
            score += 100.0
        elif g_low in o_low:
            score += 50.0

        return score

    def score_tool_candidates(
        self,
        goal: str,
        tools_metadata: List[Dict[str, Any]],
        provided_kwargs: Dict[str, Any],
    ) -> List[Tuple[float, str]]:
        """
        Calculates match scores for tools based on a goal/capability.
        Returns a sorted list of (score, tool_name).
        """
        g_low: str = goal.lower()
        scored_candidates: List[Tuple[float, str]] = []

        for t in tools_metadata:
            name = t.get("name", "")
            owner = t.get("owner", "")

            # Use cached core logic for speed (Phase 107 optimization)
            score = self.cached_logic_match(goal, name, owner)

            params: Dict[str, Any] = t.get("parameters", {})

            # Bonus for parameter intersection
            for param_name in provided_kwargs:
                if param_name in params:
                    score += 20.0

            # Penalty for excessive owner name length (prefer shorter specific names)
            score -= len(owner) / 10.0

            if score >= float(self.default_score_threshold):
                scored_candidates.append((score, name))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates

    def validate_state_transition(self, current_state: str, next_state: str) -> bool:
        """Logic for allowed workflow state transitions."""
        allowed = {
            "IDLE": ["PLANNING", "TERMINATED"],
            "PLANNING": ["EXECUTING", "ERROR"],
            "EXECUTING": ["REVIEWING", "ERROR"],
            "REVIEWING": ["IDLE", "PLANNING", "ERROR"],
            "ERROR": ["PLANNING", "IDLE"],
        }
        return next_state in allowed.get(current_state, [])
