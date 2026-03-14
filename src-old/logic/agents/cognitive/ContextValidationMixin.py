#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/ContextValidationMixin.description.md

# ContextValidationMixin

**File**: `src\\logic\agents\\cognitive\\ContextValidationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ContextValidationMixin.

## Classes (1)

### `ContextValidationMixin`

Validation methods for ContextAgent.

**Methods** (3):
- `add_validation_rule(self, rule)`
- `validate_content(self, content)`
- `is_valid(self, content)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `re`
- `src.core.base.models.ValidationRule`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/ContextValidationMixin.improvements.md

# Improvements for ContextValidationMixin

**File**: `src\\logic\agents\\cognitive\\ContextValidationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextValidationMixin_test.py` with pytest tests

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


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
import re
from typing import Any

from src.core.base.models import ValidationRule

# Default validation rules
DEFAULT_VALIDATION_RULES: list[ValidationRule] = [
    ValidationRule(
        name="has_purpose",
        pattern=r"##\s*Purpose\b",
        message="Context should have a Purpose section",
        severity="error",
        required=True,
    ),
    ValidationRule(
        name="no_empty_sections",
        pattern=r"##\s*\w+\s*\n\s*\n##",
        message="Empty section detected",
        severity="warning",
    ),
    ValidationRule(
        name="valid_code_blocks",
        pattern=r"```\w*\n[\s\S]*?```",
        message="Code blocks should have language identifier",
        severity="info",
    ),
]


class ContextValidationMixin:
    """
    """
