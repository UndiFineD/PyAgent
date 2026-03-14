# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

r"""LLM_CONTEXT_START

## Source: src-old/core/base/parsers/reasoning/__init__.description.md

# __init__

**File**: `src\\core\base\\parsers\reasoning\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 11 imports  
**Lines**: 35  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for __init__.

## Dependencies

**Imports** (11):
- `base.ReasoningParser`
- `implementations.identity.IdentityReasoningParser`
- `implementations.json.JSONReasoningParser`
- `implementations.markdown.MarkdownReasoningParser`
- `implementations.xml.XMLReasoningParser`
- `models.ReasoningResult`
- `models.StreamingReasoningState`
- `registry.ReasoningParserManager`
- `registry.reasoning_parser`
- `utils.create_streaming_parser`
- `utils.extract_reasoning`

---
*Auto-generated documentation*
## Source: src-old/core/base/parsers/reasoning/__init__.improvements.md

# Improvements for __init__

**File**: `src\\core\base\\parsers\reasoning\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 35 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

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

from .base import ReasoningParser
from .implementations.identity import IdentityReasoningParser
from .implementations.json import JSONReasoningParser
from .implementations.markdown import MarkdownReasoningParser
from .implementations.xml import XMLReasoningParser
from .models import ReasoningResult, StreamingReasoningState
from .registry import ReasoningParserManager, reasoning_parser
from .utils import create_streaming_parser, extract_reasoning

# Register built-in parsers
ReasoningParserManager.register_module("xml", XMLReasoningParser)
ReasoningParserManager.register_module("json", JSONReasoningParser)
ReasoningParserManager.register_module("markdown", MarkdownReasoningParser)
ReasoningParserManager.register_module("identity", IdentityReasoningParser)

# Aliases
ReasoningParserManager.register_module("think", XMLReasoningParser)
ReasoningParserManager.register_module("none", IdentityReasoningParser)

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
