# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/implementations/identity.description.md

# identity

**File**: `src\\core\base\\parsers\reasoning\\implementations\\identity.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 45  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for identity.

## Classes (1)

### `IdentityReasoningParser`

**Inherits from**: ReasoningParser

No-op parser that returns the full output as content.

**Methods** (4):
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (6):
- `base.ReasoningParser`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/implementations/identity.improvements.md

# Improvements for identity

**File**: `src\\core\base\\parsers\reasoning\\implementations\\identity.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `identity_test.py` with pytest tests

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

from typing import Any, ClassVar, Sequence

from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class IdentityReasoningParser(ReasoningParser):
    """No-op parser that returns the full output as content.
    """

    name: ClassVar[str] = "identity"

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        return True

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        return input_ids

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        return ReasoningResult(content=model_output)

    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()

        state.accumulated_text = current_text
        state.content_buffer = current_text

        return ReasoningResult(content=delta_text), state
