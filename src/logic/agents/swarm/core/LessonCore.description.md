# LessonCore

**File**: `src\logic\agents\swarm\core\LessonCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 42  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for LessonCore.

## Classes (2)

### `Lesson`

Class Lesson implementation.

### `LessonCore`

Pure logic for cross-fleet lesson aggregation.
Uses bloom-filter-like hashing to track known failure modes.

**Methods** (5):
- `__init__(self)`
- `generate_failure_hash(self, error_msg)`
- `is_known_failure(self, error_msg)`
- `record_lesson(self, lesson)`
- `get_related_lessons(self, error_msg, all_lessons)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `hashlib`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
