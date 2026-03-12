"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/AccessibilityCoreMixin.description.md

# AccessibilityCoreMixin

**File**: `src\logic\agents\development\mixins\AccessibilityCoreMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 82  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AccessibilityCoreMixin.

## Classes (1)

### `AccessibilityCoreMixin`

Mixin for core accessibility calculations and filtering in AccessibilityAgent.

**Methods** (4):
- `check_color_contrast(self, foreground, background, is_large_text)`
- `_relative_luminance(self, hex_color)`
- `get_issues_by_severity(self, severity)`
- `get_issues_by_wcag_level(self, level)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.types.AccessibilityIssue.AccessibilityIssue`
- `src.core.base.types.AccessibilitySeverity.AccessibilitySeverity`
- `src.core.base.types.ColorContrastResult.ColorContrastResult`
- `src.core.base.types.WCAGLevel.WCAGLevel`
- `src.logic.agents.development.AccessibilityAgent.AccessibilityAgent`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/AccessibilityCoreMixin.improvements.md

# Improvements for AccessibilityCoreMixin

**File**: `src\logic\agents\development\mixins\AccessibilityCoreMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 82 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AccessibilityCoreMixin_test.py` with pytest tests

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
from src.logic.agents.development.AccessibilityAgent import AccessibilityAgent

from typing import TYPE_CHECKING
from src.core.base.types.ColorContrastResult import ColorContrastResult
from src.core.base.types.AccessibilitySeverity import AccessibilitySeverity
from src.core.base.types.WCAGLevel import WCAGLevel
from src.core.base.types.AccessibilityIssue import AccessibilityIssue

class AccessibilityCoreMixin:
    """Mixin for core accessibility calculations and filtering in AccessibilityAgent."""

    def check_color_contrast(
        self: AccessibilityAgent,
        foreground: str,
        background: str,
        is_large_text: bool = False,
    ) -> ColorContrastResult:
        """Check color contrast ratio.

        Args:
            foreground: Foreground color (hex).
            background: Background color (hex).
            is_large_text: Whether text is large (14pt bold or 18pt+).

        Returns:
            Color contrast analysis result.
        """
        fg_luminance = self._relative_luminance(foreground)
        bg_luminance = self._relative_luminance(background)

        lighter = max(fg_luminance, bg_luminance)
        darker = min(fg_luminance, bg_luminance)
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)

        # WCAG AA: 4.5:1 for normal text, 3:1 for large text
        # WCAG AAA: 7:1 for normal text, 4.5:1 for large text
        min_aa = 3.0 if is_large_text else 4.5
        min_aaa = 4.5 if is_large_text else 7.0

        return ColorContrastResult(
            foreground=foreground,
            background=background,
            contrast_ratio=round(contrast_ratio, 2),
            passes_aa=contrast_ratio >= min_aa,
            passes_aaa=contrast_ratio >= min_aaa,
            min_ratio_aa=min_aa,
            min_ratio_aaa=min_aaa,
        )

    def _relative_luminance(self: AccessibilityAgent, hex_color: str) -> float:
        """Calculate relative luminance of a color.

        Args:
            hex_color: Hex color string (e.g., "#FFFFFF").

        Returns:
            Relative luminance value.
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])

        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255

        def adjust(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    def get_issues_by_severity(
        self: AccessibilityAgent, severity: AccessibilitySeverity
    ) -> list[AccessibilityIssue]:
        """Get issues filtered by severity."""
        return [i for i in self.issues if i.severity == severity]

    def get_issues_by_wcag_level(
        self: AccessibilityAgent, level: WCAGLevel
    ) -> list[AccessibilityIssue]:
        """Get issues filtered by WCAG level."""
        return [i for i in self.issues if i.wcag_level == level]
