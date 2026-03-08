# RefactoringAdvisor

**File**: `src\classes\context\RefactoringAdvisor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 122  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `RefactoringAdvisor`

Suggests refactoring based on context analysis.

Analyzes context to suggest code refactoring opportunities.

Example:
    >>> advisor=RefactoringAdvisor()
    >>> suggestions=advisor.analyze(contexts)

**Methods** (4):
- `__init__(self)`
- `add_pattern(self, name, pattern, description)`
- `analyze(self, contexts)`
- `prioritize(self, suggestions)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.RefactoringSuggestion.RefactoringSuggestion`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
