# GraphEntityMixin

**File**: `src\logic\agents\cognitive\mixins\GraphEntityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 82  
**Complexity**: 4 (simple)

## Overview

Entity and relationship logic for GraphMemoryAgent.

## Classes (1)

### `GraphEntityMixin`

Mixin for entity and relationship management.

**Methods** (4):
- `add_entity(self, name, properties, entity_type)`
- `add_relationship(self, subject, predicate, object_)`
- `query_relationships(self, entity_name)`
- `hybrid_search(self, query)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseUtilities.as_tool`
- `typing.Any`

---
*Auto-generated documentation*
