# MapBuilderMixin

**File**: `src\logic\agents\system\mixins\MapBuilderMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for MapBuilderMixin.

## Classes (1)

### `MapBuilderMixin`

Mixin for mapping and parsing code entities in TopologicalNavigator.

**Methods** (3):
- `_get_entity_id(self, file_path, entity_name)`
- `build_dependency_map(self, target_dir)`
- `_parse_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `ast`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.system.TopologicalNavigator.TopologicalNavigator`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
