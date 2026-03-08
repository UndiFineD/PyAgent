"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/base.description.md

# base

**File**: `src\core\base\parsers\reasoning\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 131  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for base.

## Classes (1)

### `ReasoningParser`

**Inherits from**: ABC

Abstract reasoning parser class for extracting reasoning from model outputs.

Subclasses must implement:
- is_reasoning_end: Check if reasoning section has ended
- extract_content_ids: Extract content token IDs from full output
- extract_reasoning: Extract reasoning from complete output
- extract_reasoning_streaming: Extract reasoning incrementally

Attributes:
    tokenizer: The tokenizer used for token-level operations.

**Methods** (7):
- `__init__(self, tokenizer)`
- `vocab(self)`
- `is_reasoning_end(self, input_ids)`
- `is_reasoning_end_streaming(self, input_ids, delta_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `functools.cached_property`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/base.improvements.md

# Improvements for base

**File**: `src\core\base\parsers\reasoning\base.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_test.py` with pytest tests

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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Sequence
from functools import cached_property
from .models import ReasoningResult, StreamingReasoningState


class ReasoningParser(ABC):
    """
    Abstract reasoning parser class for extracting reasoning from model outputs.

    Subclasses must implement:
    - is_reasoning_end: Check if reasoning section has ended
    - extract_content_ids: Extract content token IDs from full output
    - extract_reasoning: Extract reasoning from complete output
    - extract_reasoning_streaming: Extract reasoning incrementally

    Attributes:
        tokenizer: The tokenizer used for token-level operations.
    """

    # Class-level name for registration
    name: ClassVar[str] = "base"

    def __init__(self, tokenizer: Any = None, **kwargs: Any) -> None:
        """
        Initialize the reasoning parser.

        Args:
            tokenizer: Tokenizer for token-level operations (optional).
            **kwargs: Additional configuration options.
        """
        self.model_tokenizer = tokenizer

    @cached_property
    def vocab(self) -> dict[str, int]:
        """Get tokenizer vocabulary."""
        if self.model_tokenizer is None:
            return {}
        # Support both .vocab and .get_vocab()
        if hasattr(self.model_tokenizer, "get_vocab"):
            return self.model_tokenizer.get_vocab()
        return getattr(self.model_tokenizer, "vocab", {})

    @abstractmethod
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        """
        Check if the reasoning content ends in the input_ids.

        Args:
            input_ids: The token IDs of the model output.

        Returns:
            True if reasoning section has ended.
        """

    def is_reasoning_end_streaming(
        self,
        input_ids: list[int],
        delta_ids: list[int],
    ) -> bool:
        """
        Check if reasoning ends during streaming (decode step).

        Args:
            input_ids: The entire model output token IDs.
            delta_ids: The latest tokens from current decode step.

        Returns:
            True if reasoning section ends in delta_ids.
        """
        return self.is_reasoning_end(input_ids)

    @abstractmethod
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        """
        Extract content token IDs from the full output.

        Args:
            input_ids: The token IDs of the model output.

        Returns:
            Token IDs for the content/answer portion.
        """

    @abstractmethod
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        """
        Extract reasoning content from a complete model output.

        Args:
            model_output: The complete model-generated string.
            request: Optional request object for context.

        Returns:
            ReasoningResult with extracted reasoning and content.
        """

    @abstractmethod
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
        """
        Extract reasoning incrementally during streaming.

        Args:
            previous_text: Text accumulated before this step.
            current_text: Text accumulated including this step.
            delta_text: New text from this step.
            previous_token_ids: Token IDs before this step.
            current_token_ids: Token IDs including this step.
            delta_token_ids: New token IDs from this step.
            state: Previous streaming state (or None for first call).

        Returns:
            Tuple of (incremental result, updated state).
        """
