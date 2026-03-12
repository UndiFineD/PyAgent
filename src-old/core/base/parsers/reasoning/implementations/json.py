# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/implementations/json.description.md

# json

**File**: `src\\core\base\\parsers\reasoning\\implementations\\json.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for json.

## Classes (1)

### `JSONReasoningParser`

**Inherits from**: ReasoningParser

Parser for JSON-structured reasoning outputs.

Expects output in format:
{"reasoning": "...", "answer": "..."}

**Methods** (5):
- `__init__(self, tokenizer)`
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (8):
- `base.ReasoningParser`
- `json`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `re`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/implementations/json.improvements.md

# Improvements for json

**File**: `src\\core\base\\parsers\reasoning\\implementations\\json.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 102 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `json_test.py` with pytest tests

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

import json
import re
from typing import Any, ClassVar, Sequence

from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class JSONReasoningParser(ReasoningParser):
    """Parser for JSON-structured reasoning outputs.

    Expects output in format:
    {"reasoning": "...", "answer": "..."}
    """

    name: ClassVar[str] = "json"

    def __init__(
        self,
        tokenizer: Any = None,
        *,
        reasoning_key: str = "reasoning",
        answer_key: str = "answer",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.reasoning_key = reasoning_key
        self.answer_key = answer_key

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete JSON
        try:
            data = json.loads(text)
            return self.answer_key in data
        except json.JSONDecodeError:
            return False

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids

        text = self.model_tokenizer.decode(input_ids)
        result = self.extract_reasoning(text)
        if result.content:
            return self.model_tokenizer.encode(result.content, add_special_tokens=False)
        return input_ids

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        try:
            data = json.loads(model_output)
            return ReasoningResult(
                reasoning=data.get(self.reasoning_key),
                content=data.get(self.answer_key),
            )
        except json.JSONDecodeError:
            # Try to extract JSON from text
            match = re.search(r"\{[^{}]*\}", model_output, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                    return ReasoningResult(
                        reasoning=data.get(self.reasoning_key),
                        content=data.get(self.answer_key),
                    )
                except json.JSONDecodeError:
                    pass

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

        # Try to parse as JSON
        result = self.extract_reasoning(current_text)
        if result.reasoning or result.content:
            state.reasoning_buffer = result.reasoning or ""
            state.content_buffer = result.content or ""
            state.reasoning_complete = True

        return result, state
