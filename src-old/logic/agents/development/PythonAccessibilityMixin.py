#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/PythonAccessibilityMixin.description.md

# PythonAccessibilityMixin

**File**: `src\logic\agents\development\PythonAccessibilityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 45  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for PythonAccessibilityMixin.

## Classes (1)

### `PythonAccessibilityMixin`

Mixin for Python UI accessibility analysis.

**Methods** (1):
- `_analyze_python_ui(self, content)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.types.AccessibilityIssue.AccessibilityIssue`
- `src.core.base.types.AccessibilityIssueType.AccessibilityIssueType`
- `src.core.base.types.AccessibilitySeverity.AccessibilitySeverity`
- `src.core.base.types.WCAGLevel.WCAGLevel`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/PythonAccessibilityMixin.improvements.md

# Improvements for PythonAccessibilityMixin

**File**: `src\logic\agents\development\PythonAccessibilityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PythonAccessibilityMixin_test.py` with pytest tests

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

# Copyright 2026 PyAgent Authors

import re
from src.core.base.types.AccessibilityIssue import AccessibilityIssue
from src.core.base.types.AccessibilityIssueType import AccessibilityIssueType
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.WCAGLevel import WCAGLevel


class PythonAccessibilityMixin:
    """Mixin for Python UI accessibility analysis."""

    def _analyze_python_ui(self, content: str) -> None:
        """Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues."""
        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (r"Button\s*\([^)]*\)", "Button"),
            (r"Label\s*\([^)]*\)", "Label"),
            (r"Entry\s*\([^)]*\)", "Entry"),
            (r"Canvas\s*\([^)]*\)", "Canvas"),
        ]
        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[: match.start()].count("\n") + 1

                # Check for tooltips / accessibility text
                if (
                    "tooltip" not in widget_call.lower()
                    and "help" not in widget_call.lower()
                ):
                    self.issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.ARIA_MISSING,
                            severity=AccessibilitySeverity.MINOR,
                            wcag_level=WCAGLevel.AA,
                            wcag_criterion="4.1.2",
                            description=f"{widget_name} widget may benefit from tooltip or help text",
                            element=widget_call[:50],
                            line_number=line_num,
                            suggested_fix="Consider adding tooltip or accessibility description",
                            auto_fixable=False,
                        )
                    )
