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
