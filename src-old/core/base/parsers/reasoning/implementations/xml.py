# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/implementations/xml.description.md

# xml

**File**: `src\core\base\parsers\reasoning\implementations\xml.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 116  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for xml.

## Classes (1)

### `XMLReasoningParser`

**Inherits from**: ReasoningParser

Parser for XML-style think blocks.

Extracts reasoning from <think>...</think> or <reasoning>...</reasoning> tags.

**Methods** (6):
- `__init__(self, tokenizer)`
- `is_reasoning_end(self, input_ids)`
- `extract_content_ids(self, input_ids)`
- `_extract_content(self, text)`
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
## Source: src-old/core/base/parsers/reasoning/implementations/xml.improvements.md

# Improvements for xml

**File**: `src\core\base\parsers\reasoning\implementations\xml.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `xml_test.py` with pytest tests

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

import re
from typing import Any, ClassVar, Sequence
from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class XMLReasoningParser(ReasoningParser):
    """
    Parser for XML-style think blocks.

    Extracts reasoning from <think>...</think> or <reasoning>...</reasoning> tags.
    """

    name: ClassVar[str] = "xml"

    def __init__(
        self,
        tokenizer: Any = None,
        *,
        start_tag: str = "<think>",
        end_tag: str = "</think>",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.start_tag = start_tag
        self.end_tag = end_tag
        self._pattern = re.compile(
            rf"{re.escape(start_tag)}(.*?){re.escape(end_tag)}",
            re.DOTALL,
        )

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        return self.end_tag in text

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids

        text = self.model_tokenizer.decode(input_ids)
        content = self._extract_content(text)
        return self.model_tokenizer.encode(content, add_special_tokens=False)

    def _extract_content(self, text: str) -> str:
        """Extract content after removing think blocks."""
        # Remove all think blocks
        content = self._pattern.sub("", text)
        return content.strip()

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        # Find all think blocks
        matches = self._pattern.findall(model_output)
        reasoning = "\n".join(matches) if matches else None

        # Get content without think blocks
        content = self._extract_content(model_output)

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
        state.accumulated_tokens = list(current_token_ids)

        # Check for start of reasoning
        if self.start_tag in current_text and not state.in_reasoning:
            state.in_reasoning = True
            # Extract text before start tag as content
            before_tag = current_text.split(self.start_tag)[0]
            state.content_buffer = before_tag

        # Check for end of reasoning
        if self.end_tag in current_text and state.in_reasoning:
            state.in_reasoning = False
            state.reasoning_complete = True

            # Extract the full reasoning
            match = self._pattern.search(current_text)
            if match:
                state.reasoning_buffer = match.group(1)

            # Get content after end tag
            after_tag = current_text.split(self.end_tag)[-1]
            state.content_buffer += after_tag
        elif state.reasoning_complete:
            # After reasoning is complete, accumulate content
            state.content_buffer = self._extract_content(current_text)

        return (
            ReasoningResult(
                reasoning=state.reasoning_buffer if state.reasoning_buffer else None,
                content=state.content_buffer if state.content_buffer else None,
                is_complete=state.reasoning_complete and self.end_tag in current_text,
            ),
            state,
        )
