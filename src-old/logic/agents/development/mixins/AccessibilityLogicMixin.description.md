# AccessibilityLogicMixin

**File**: `src\logic\agents\development\mixins\AccessibilityLogicMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 52  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AccessibilityLogicMixin.

## Classes (1)

### `AccessibilityLogicMixin`

Mixin for entry-point analysis logic and rule management in AccessibilityAgent.

**Methods** (4):
- `analyze_file(self, file_path)`
- `analyze_content(self, content, file_type)`
- `enable_rule(self, wcag_criterion)`
- `disable_rule(self, wcag_criterion)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.types.AccessibilityReport.AccessibilityReport`
- `src.logic.agents.development.AccessibilityAgent.AccessibilityAgent`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
