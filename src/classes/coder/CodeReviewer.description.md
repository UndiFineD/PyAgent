# CodeReviewer

**File**: `src\classes\coder\CodeReviewer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 121  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `CodeReviewer`

Automated code review system.

Provides automated code review with actionable suggestions
across multiple categories.

Attributes:
    findings: List of review findings.

Example:
    >>> reviewer=CodeReviewer()
    >>> findings=reviewer.review_code("def foo():\n    pass")

**Methods** (3):
- `__init__(self)`
- `review_code(self, content)`
- `get_summary(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.types.ReviewCategory.ReviewCategory`
- `src.core.base.types.ReviewFinding.ReviewFinding`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
