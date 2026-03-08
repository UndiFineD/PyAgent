# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/utils.description.md

# utils

**File**: `src\core\base\parsers\reasoning\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 4 imports  
**Lines**: 32  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for utils.

## Functions (2)

### `extract_reasoning(model_output, parser_name, tokenizer)`

Convenience function to extract reasoning from model output.

### `create_streaming_parser(parser_name, tokenizer)`

Create a parser and state for streaming extraction.

## Dependencies

**Imports** (4):
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `registry.ReasoningParserManager`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/utils.improvements.md

# Improvements for utils

**File**: `src\core\base\parsers\reasoning\utils.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `utils_test.py` with pytest tests

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

from typing import Any
from .registry import ReasoningParserManager
from .models import ReasoningResult, StreamingReasoningState


def extract_reasoning(
    model_output: str,
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> ReasoningResult:
    """
    Convenience function to extract reasoning from model output.
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    return parser.extract_reasoning(model_output)


def create_streaming_parser(
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> tuple[Any, StreamingReasoningState]:
    """
    Create a parser and state for streaming extraction.
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    state = StreamingReasoningState()
    return parser, state
