#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/JavascriptAccessibilityMixin.description.md

# JavascriptAccessibilityMixin

**File**: `src\logic\agents\development\JavascriptAccessibilityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 56  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for JavascriptAccessibilityMixin.

## Classes (1)

### `JavascriptAccessibilityMixin`

Mixin for Javascript UI accessibility analysis.

**Methods** (1):
- `_analyze_javascript_ui(self, content)`

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
## Source: src-old/logic/agents/development/JavascriptAccessibilityMixin.improvements.md

# Improvements for JavascriptAccessibilityMixin

**File**: `src\logic\agents\development\JavascriptAccessibilityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 56 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `JavascriptAccessibilityMixin_test.py` with pytest tests

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

import re
from src.core.base.types.AccessibilityIssue import AccessibilityIssue
from src.core.base.types.AccessibilityIssueType import AccessibilityIssueType
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.WCAGLevel import WCAGLevel


class JavascriptAccessibilityMixin:
    """Mixin for Javascript UI accessibility analysis."""

    def _analyze_javascript_ui(self, content: str) -> None:
        """Analyze JavaScript / React UI code for accessibility issues."""
        # Check for click handlers without keyboard support
        click_pattern = r"onClick\s*=\s*\{[^}]+\}"
        for match in re.finditer(click_pattern, content):
            line_num = content[: match.start()].count("\n") + 1
            # Check if there's also onKeyPress / onKeyDown nearby
            context = content[max(0, match.start() - 100) : match.end() + 100]
            if "onKeyPress" not in context and "onKeyDown" not in context:
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.KEYBOARD_NAVIGATION,
                        severity=AccessibilitySeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        wcag_criterion="2.1.1",
                        description="Click handler without keyboard equivalent",
                        element=match.group()[:50],
                        line_number=line_num,
                        suggested_fix="Add onKeyPress or onKeyDown handler for keyboard users",
                        auto_fixable=False,
                    )
                )

        # Check for div / span used as interactive elements
        interactive_div = r"<div\b[^>]*\bonClick\s*=\s*\{[^}]+\}[^>]*>"
        for match in re.finditer(interactive_div, content, re.IGNORECASE):
            line_num = content[: match.start()].count("\n") + 1
            context = match.group()
            context_lower = context.lower()
            if "role=" not in context_lower and "tabindex" not in context_lower:
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.SEMANTIC_HTML,
                        severity=AccessibilitySeverity.SERIOUS,
                        wcag_level=WCAGLevel.A,
                        wcag_criterion="1.3.1",
                        description="Interactive div should be a button or have role / tabIndex",
                        element=context[:50],
                        line_number=line_num,
                        suggested_fix='Use <button> or add role="button" tabIndex="0"',
                        auto_fixable=False,
                    )
                )
