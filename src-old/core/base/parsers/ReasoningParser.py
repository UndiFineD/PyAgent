# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
r"""LLM_CONTEXT_START

## Source: src-old/core/base/parsers/ReasoningParser.description.md

# ReasoningParser

**File**: `src\\core\base\\parsers\\ReasoningParser.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 11 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

ReasoningParser - Extensible framework for extracting reasoning from LLM outputs.
(Facade for modular implementation)

## Dependencies

**Imports** (11):
- `reasoning.IdentityReasoningParser`
- `reasoning.JSONReasoningParser`
- `reasoning.MarkdownReasoningParser`
- `reasoning.ReasoningParser`
- `reasoning.ReasoningParserManager`
- `reasoning.ReasoningResult`
- `reasoning.StreamingReasoningState`
- `reasoning.XMLReasoningParser`
- `reasoning.create_streaming_parser`
- `reasoning.extract_reasoning`
- `reasoning.reasoning_parser`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/ReasoningParser.improvements.md

# Improvements for ReasoningParser

**File**: `src\\core\base\\parsers\\ReasoningParser.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReasoningParser_test.py` with pytest tests

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
ReasoningParser - Extensible framework for extracting reasoning from LLM outputs.
(Facade for modular implementation)
"""

from .reasoning import (
    IdentityReasoningParser,
    JSONReasoningParser,
    MarkdownReasoningParser,
    ReasoningParser,
    ReasoningParserManager,
    ReasoningResult,
    StreamingReasoningState,
    XMLReasoningParser,
    create_streaming_parser,
    extract_reasoning,
    reasoning_parser,
)

__all__ = [
    "ReasoningResult",
    "StreamingReasoningState",
    "ReasoningParser",
    "ReasoningParserManager",
    "reasoning_parser",
    "extract_reasoning",
    "create_streaming_parser",
    "XMLReasoningParser",
    "JSONReasoningParser",
    "MarkdownReasoningParser",
    "IdentityReasoningParser",
]
