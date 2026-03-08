# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/models.description.md

# models

**File**: `src\core\base\parsers\reasoning\models.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 2 imports  
**Lines**: 37  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for models.

## Classes (2)

### `ReasoningResult`

Result of reasoning extraction.

Attributes:
    reasoning: The extracted reasoning/thinking content.
    content: The extracted content/answer.
    reasoning_tokens: Token IDs for reasoning (if available).
    content_tokens: Token IDs for content (if available).
    is_complete: Whether reasoning extraction is complete.

### `StreamingReasoningState`

State for streaming reasoning extraction.

Tracks the current state of reasoning extraction during streaming.

## Dependencies

**Imports** (2):
- `dataclasses.dataclass`
- `dataclasses.field`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/models.improvements.md

# Improvements for models

**File**: `src\core\base\parsers\reasoning\models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 37 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `models_test.py` with pytest tests

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

from dataclasses import dataclass, field

@dataclass
class ReasoningResult:
    """
    Result of reasoning extraction.
    
    Attributes:
        reasoning: The extracted reasoning/thinking content.
        content: The extracted content/answer.
        reasoning_tokens: Token IDs for reasoning (if available).
        content_tokens: Token IDs for content (if available).
        is_complete: Whether reasoning extraction is complete.
    """
    reasoning: str | None = None
    content: str | None = None
    reasoning_tokens: list[int] | None = None
    content_tokens: list[int] | None = None
    is_complete: bool = True


@dataclass
class StreamingReasoningState:
    """
    State for streaming reasoning extraction.
    
    Tracks the current state of reasoning extraction during streaming.
    """
    accumulated_text: str = ""
    accumulated_tokens: list[int] = field(default_factory=list)
    in_reasoning: bool = False
    reasoning_buffer: str = ""
    content_buffer: str = ""
    reasoning_complete: bool = False
