# Class Breakdown: models

**File**: `src\infrastructure\backend\llm_backends\lmstudio\models.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LMStudioConfig`

**Line**: 14  
**Methods**: 1

Configuration for LM Studio connection.

[TIP] **Suggested split**: Move to `lmstudioconfig.py`

---

### 2. `CachedModel`

**Line**: 45  
**Methods**: 2

Cached model reference with TTL.

[TIP] **Suggested split**: Move to `cachedmodel.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
