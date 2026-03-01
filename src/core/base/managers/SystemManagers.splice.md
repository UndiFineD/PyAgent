# Class Breakdown: SystemManagers

**File**: `src\core\base\managers\SystemManagers.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FilePriorityManager`

**Line**: 45  
**Methods**: 6

Manager for file priority and request ordering.

[TIP] **Suggested split**: Move to `fileprioritymanager.py`

---

### 2. `ResponseCache`

**Line**: 75  
**Methods**: 5

Caches responses based on prompts. 
Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.

[TIP] **Suggested split**: Move to `responsecache.py`

---

### 3. `StatePersistence`

**Line**: 131  
**Methods**: 2

Persists agent state to disk.

[TIP] **Suggested split**: Move to `statepersistence.py`

---

### 4. `EventManager`

**Line**: 148  
**Methods**: 2

Manages agent events.

[TIP] **Suggested split**: Move to `eventmanager.py`

---

### 5. `HealthChecker`

**Line**: 163  
**Methods**: 10

Performs health checks on agent components.

[TIP] **Suggested split**: Move to `healthchecker.py`

---

### 6. `ProfileManager`

**Line**: 269  
**Methods**: 8

Manages configuration profiles and execution profiles.

[TIP] **Suggested split**: Move to `profilemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
