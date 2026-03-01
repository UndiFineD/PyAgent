# ContextCategorizationMixin

**File**: `src\logic\agents\cognitive\ContextCategorizationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 127  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for ContextCategorizationMixin.

## Classes (1)

### `ContextCategorizationMixin`

Categorization, priority, and metadata methods for ContextAgent.

**Methods** (10):
- `set_priority(self, priority)`
- `get_priority(self)`
- `calculate_priority_score(self)`
- `set_category(self, category)`
- `get_category(self)`
- `auto_categorize(self)`
- `set_metadata(self, key, value)`
- `get_metadata(self, key)`
- `get_all_metadata(self)`
- `export_metadata(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `json`
- `re`
- `src.logic.agents.cognitive.context.models.ContextPriority.ContextPriority`
- `src.logic.agents.cognitive.context.models.FileCategory.FileCategory`
- `typing.Any`

---
*Auto-generated documentation*
