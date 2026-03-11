#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextRecommendation.description.md

# ContextRecommendation

**File**: `src\classes\context\ContextRecommendation.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextRecommendation`

Recommendation for context improvement.

Attributes:
    source_file: File used as reference.
    suggested_sections: Sections to add.
    reason: Why this recommendation was made.
    confidence: Recommendation confidence.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextRecommendation.improvements.md

# Improvements for ContextRecommendation

**File**: `src\classes\context\ContextRecommendation.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextRecommendation_test.py` with pytest tests

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

"""Auto-extracted class from agent_context.py"""


from dataclasses import dataclass, field
from typing import List


@dataclass
class ContextRecommendation:
    """Recommendation for context improvement.

    Attributes:
        source_file: File used as reference.
        suggested_sections: Sections to add.
        reason: Why this recommendation was made.
        confidence: Recommendation confidence.

    """

    source_file: str
    suggested_sections: List[str] = field(default_factory=lambda: [])
    reason: str = ""
    confidence: float = 0.0
