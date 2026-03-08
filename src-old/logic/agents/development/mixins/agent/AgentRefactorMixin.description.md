# AgentRefactorMixin

**File**: `src\logic\agents\development\mixins\agent\AgentRefactorMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 75  
**Complexity**: 5 (moderate)

## Overview

Refactoring pattern and duplication logic for CoderAgent.

## Classes (1)

### `AgentRefactorMixin`

Mixin for code deduplication and refactoring patterns.

**Methods** (5):
- `find_duplicate_code(self, content, min_lines)`
- `get_duplicate_ratio(self, content)`
- `add_refactoring_pattern(self, pattern)`
- `apply_refactoring_patterns(self, content)`
- `suggest_refactorings(self, content)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `re`
- `src.core.base.types.RefactoringPattern.RefactoringPattern`
- `typing.Any`

---
*Auto-generated documentation*
