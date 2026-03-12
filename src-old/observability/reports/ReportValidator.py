#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/ReportValidator.description.md

# ReportValidator

**File**: `src\\observability\reports\\ReportValidator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from generate_agent_reports.py

## Classes (1)

### `ReportValidator`

Validator for report data integrity.
Validates report structure, content, and checksums.

Example:
    validator=ReportValidator()
    result=validator.validate(content)
    if not result.valid:
        print(result.errors)

**Methods** (3):
- `__init__(self)`
- `validate(self, content)`
- `verify_checksum(self, content, expected)`

## Dependencies

**Imports** (7):
- `ValidationResult.ValidationResult`
- `__future__.annotations`
- `hashlib`
- `logging`
- `re`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/reports/ReportValidator.improvements.md

# Improvements for ReportValidator

**File**: `src\\observability\reports\\ReportValidator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReportValidator_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Auto-extracted class from generate_agent_reports.py"""

import hashlib
import logging
import re

from src.core.base.version import VERSION

from .ValidationResult import ValidationResult

__version__ = VERSION


class ReportValidator:
    """Validator for report data integrity.
    Validates report structure, content, and checksums.

    Example:
        validator=ReportValidator()
        result=validator.validate(content)
        if not result.valid:
            print(result.errors)

    """

    def __init__(self) -> None:
        """Initialize validator."""
        logging.debug("ReportValidator initialized")

    def validate(self, content: str) -> ValidationResult:
        """Validate report content.

        Args:
            content: Report content.

        Returns:
            Validation result.

        """
        errors: list[str] = []
        warnings: list[str] = []
        # Check for required sections
        if not re.search(r"^#+\s", content, re.MULTILINE):
            errors.append("Missing main heading")
        # Check for empty content
        if len(content.strip()) < 10:
            errors.append("Content too short")
        # Check for malformed links
        if re.search(r"\[.*?\]\(\s*\)", content):
            warnings.append("Contains empty link targets")
        # Calculate checksum
        checksum = hashlib.sha256(content.encode()).hexdigest()[:16]
        return ValidationResult(
            valid=len(errors) == 0, errors=errors, warnings=warnings, checksum=checksum
        )

    def verify_checksum(self, content: str, expected: str) -> bool:
        """Verify content checksum.

        Args:
            content: Report content.
            expected: Expected checksum.

        Returns:
            True if matches.

        """
        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected
