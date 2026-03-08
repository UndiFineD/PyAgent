# Class Breakdown: LessonCore

**File**: `src\logic\agents\swarm\core\LessonCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Lesson`

**Line**: 8  
**Methods**: 0

[TIP] **Suggested split**: Move to `lesson.py`

---

### 2. `LessonCore`

**Line**: 14  
**Methods**: 5

Pure logic for cross-fleet lesson aggregation.
Uses bloom-filter-like hashing to track known failure modes.

[TIP] **Suggested split**: Move to `lessoncore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
