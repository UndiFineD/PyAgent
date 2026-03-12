#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/GeneratedCode.description.md

# GeneratedCode

**File**: `src\classes\context\GeneratedCode.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `GeneratedCode`

Context-aware generated code.

Attributes:
    language: Programming language.
    code: Generated code content.
    context_used: Context files used for generation.
    description: Description of what the code does.

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
## Source: src-old/classes/context/GeneratedCode.improvements.md

# Improvements for GeneratedCode

**File**: `src\classes\context\GeneratedCode.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GeneratedCode_test.py` with pytest tests

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

from __future__ import annotations

"""Auto-extracted class from agent_context.py"""


from dataclasses import dataclass, field
from typing import List


@dataclass
class GeneratedCode:
    """Context-aware generated code.

    Attributes:
        language: Programming language.
        code: Generated code content.
        context_used: Context files used for generation.
        description: Description of what the code does.

    """

    language: str
    code: str
    context_used: List[str] = field(default_factory=lambda: [])
    description: str = ""
