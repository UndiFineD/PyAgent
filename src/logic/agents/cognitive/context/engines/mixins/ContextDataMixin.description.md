# ContextDataMixin

**File**: `src\logic\agents\cognitive\context\engines\mixins\ContextDataMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 98  
**Complexity**: 5 (moderate)

## Overview

Data manipulation logic for GlobalContextEngine.

## Classes (1)

### `ContextDataMixin`

Mixin for fundamental context data operations.

**Methods** (5):
- `get(self, category, key)`
- `set_with_conflict_resolution(self, category, key, value, strategy)`
- `add_fact(self, key, value)`
- `add_insight(self, insight, source_agent)`
- `add_constraint(self, constraint)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Any`

---
*Auto-generated documentation*
