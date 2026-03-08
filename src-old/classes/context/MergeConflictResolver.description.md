# MergeConflictResolver

**File**: `src\classes\context\MergeConflictResolver.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 104  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `MergeConflictResolver`

Resolves merge conflicts in context files.

Provides strategies for resolving conflicts during context merges.

Example:
    >>> resolver=MergeConflictResolver()
    >>> resolved=resolver.resolve(conflict, ConflictResolution.OURS)

**Methods** (5):
- `__init__(self, strategy)`
- `set_strategy(self, strategy)`
- `detect_conflicts(self, ours, theirs)`
- `resolve(self, conflict, strategy)`
- `resolve_all(self, conflicts, strategy)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.MergeConflict.MergeConflict`
- `src.logic.agents.cognitive.context.utils.ConflictResolution.ConflictResolution`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
