# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/implementations/markdown.description.md

# markdown

**File**: `src\core\base\parsers\reasoning\implementations\markdown.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 84  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for markdown.

## Classes (1)

### `MarkdownReasoningParser`

**Inherits from**: ReasoningParser

Parser for Markdown-style think blocks.

Extracts reasoning from ```thinking blocks or > prefixed lines.

**Methods** (5):
- `__init__(self, tokenizer)`
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `extract_reasoning(self, model_output, request)`
- `extract_reasoning_streaming(self, previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids, state)`

## Dependencies

**Imports** (7):
- `base.ReasoningParser`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `re`
- `typing.Any`
- `typing.ClassVar`
- `typing.Sequence`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/implementations/markdown.improvements.md

# Improvements for markdown

**File**: `src\core\base\parsers\reasoning\implementations\markdown.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 84 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `markdown_test.py` with pytest tests

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

import re
from typing import Any, ClassVar, Sequence
from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class MarkdownReasoningParser(ReasoningParser):
    """
    Parser for Markdown-style think blocks.

    Extracts reasoning from ```thinking blocks or > prefixed lines.
    """

    name: ClassVar[str] = "markdown"

    def __init__(
        self,
        tokenizer: Any = None,
        *,
        block_type: str = "thinking",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.block_type = block_type
        self._pattern = re.compile(
            rf"```{re.escape(block_type)}\n(.*?)```",
            re.DOTALL,
        )

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete thinking block
        return bool(self._pattern.search(text))

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids

        text = self.model_tokenizer.decode(input_ids)
        content = self._pattern.sub("", text).strip()
        return self.model_tokenizer.encode(content, add_special_tokens=False)

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        matches = self._pattern.findall(model_output)
        reasoning = "\n".join(matches) if matches else None
        content = self._pattern.sub("", model_output).strip()

        return ReasoningResult(
            reasoning=reasoning,
            content=content if content else None,
        )

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
        result = self.extract_reasoning(current_text)

        if result.reasoning:
            state.reasoning_buffer = result.reasoning
            state.reasoning_complete = True
        if result.content:
            state.content_buffer = result.content

        return result, state
