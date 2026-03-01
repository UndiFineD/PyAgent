# ContextInheritance

**File**: `src\classes\context\ContextInheritance.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 113  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextInheritance`

Manages context inheritance from parent files.

Provides functionality for child contexts to inherit
from parent contexts.

Example:
    >>> inheritance=ContextInheritance()
    >>> inherited=inheritance.inherit_from("parent.description.md", "child.description.md")

**Methods** (7):
- `__init__(self)`
- `set_mode(self, mode)`
- `set_parent(self, parent_path)`
- `apply(self, child_content, parent_content)`
- `get_hierarchy(self)`
- `inherit_from(self, parent_path, child_path, mode)`
- `resolve_inheritance(self, parent_content, child_content, mode)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.InheritanceMode.InheritanceMode`
- `src.logic.agents.cognitive.context.models.InheritedContext.InheritedContext`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
