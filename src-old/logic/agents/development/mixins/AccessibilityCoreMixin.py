r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/AccessibilityCoreMixin.description.md

# AccessibilityCoreMixin

**File**: `src\\logic\agents\\development\\mixins\\AccessibilityCoreMixin.py`  
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

**File**: `src\\logic\agents\\development\\mixins\\AccessibilityCoreMixin.py`  
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
