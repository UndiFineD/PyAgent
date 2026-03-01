# Class Breakdown: base_models

**File**: `src\core\base\models\base_models.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CacheEntry`

**Line**: 84  
**Methods**: 0

Cached response entry.

[TIP] **Suggested split**: Move to `cacheentry.py`

---

### 2. `AuthConfig`

**Line**: 93  
**Methods**: 0

Authentication configuration.

[TIP] **Suggested split**: Move to `authconfig.py`

---

### 3. `SerializationConfig`

**Line**: 105  
**Methods**: 0

Configuration for custom serialization.

[TIP] **Suggested split**: Move to `serializationconfig.py`

---

### 4. `FilePriorityConfig`

**Line**: 113  
**Methods**: 0

Configuration for file priority.

[TIP] **Suggested split**: Move to `filepriorityconfig.py`

---

### 5. `ExecutionCondition`

**Line**: 120  
**Methods**: 0

A condition for agent execution.

[TIP] **Suggested split**: Move to `executioncondition.py`

---

### 6. `ValidationRule`

**Line**: 127  
**Methods**: 1

Consolidated validation rule for Phase 126.

[TIP] **Suggested split**: Move to `validationrule.py`

---

### 7. `ModelConfig`

**Line**: 144  
**Methods**: 0

Model configuration.

[TIP] **Suggested split**: Move to `modelconfig.py`

---

### 8. `ConfigProfile`

**Line**: 153  
**Methods**: 1

Configuration profile.

[TIP] **Suggested split**: Move to `configprofile.py`

---

### 9. `DiffResult`

**Line**: 164  
**Methods**: 0

Result of a diff operation.

[TIP] **Suggested split**: Move to `diffresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
