# truncation

**File**: `src\infrastructure\prompt_renderer\truncation.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 88  
**Complexity**: 5 (moderate)

## Overview

Truncation management for prompt rendering.

## Classes (1)

### `TruncationManager`

Manage prompt truncation strategies.

**Methods** (5):
- `truncate(cls, tokens, max_tokens, strategy, reserve_tokens)`
- `_truncate_left(cls, tokens, target, original)`
- `_truncate_right(cls, tokens, target, original)`
- `_truncate_middle(cls, tokens, target, original)`
- `_truncate_smart(cls, tokens, target, original)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `models.TruncationResult`
- `models.TruncationStrategy`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
