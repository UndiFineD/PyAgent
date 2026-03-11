#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/ConsensusCore.description.md

# ConsensusCore

**File**: `src\classes\orchestration\ConsensusCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 42  
**Complexity**: 3 (simple)

## Overview

ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.

## Classes (1)

### `ConsensusCore`

Pure logic core for consensus protocols.

**Methods** (3):
- `__init__(self, mode)`
- `calculate_winner(self, proposals)`
- `get_agreement_score(self, proposals, winner)`

## Dependencies

**Imports** (4):
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/ConsensusCore.improvements.md

# Improvements for ConsensusCore

**File**: `src\classes\orchestration\ConsensusCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 42 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConsensusCore_test.py` with pytest tests

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
ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.
"""

from typing import Dict, List


class ConsensusCore:
    """Pure logic core for consensus protocols."""

    def __init__(self, mode: str = "plurality") -> None:
        self.mode = mode

    def calculate_winner(self, proposals: List[str]) -> str:
        """Determines the winning proposal based on voting rules."""
        if not proposals:
            return ""

        # Count identical proposals
        counts: Dict[str, int] = {}
        for p in proposals:
            counts[p] = counts.get(p, 0) + 1

        # Strategy: Most frequent, then longest as tie-breaker
        # In the future, this logic could be replaced by a Rust library
        # for high-performance string hashing and comparison.
        winner = sorted(
            proposals,
            key=lambda x: (counts[x], len(x)),
            reverse=True
        )[0]

        return winner

    def get_agreement_score(self, proposals: List[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)
