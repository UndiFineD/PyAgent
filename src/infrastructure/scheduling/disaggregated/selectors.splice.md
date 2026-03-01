# Class Breakdown: selectors

**File**: `src\infrastructure\scheduling\disaggregated\selectors.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `InstanceSelector`

**Line**: 10  
**Inherits**: ABC  
**Methods**: 1

Abstract base for instance selection strategies.

[TIP] **Suggested split**: Move to `instanceselector.py`

---

### 2. `RoundRobinSelector`

**Line**: 23  
**Inherits**: InstanceSelector  
**Methods**: 2

Round-robin instance selection.

[TIP] **Suggested split**: Move to `roundrobinselector.py`

---

### 3. `LeastLoadedSelector`

**Line**: 46  
**Inherits**: InstanceSelector  
**Methods**: 1

Select least loaded instance.

[TIP] **Suggested split**: Move to `leastloadedselector.py`

---

### 4. `RandomSelector`

**Line**: 61  
**Inherits**: InstanceSelector  
**Methods**: 1

Random instance selection.

[TIP] **Suggested split**: Move to `randomselector.py`

---

### 5. `HashSelector`

**Line**: 76  
**Inherits**: InstanceSelector  
**Methods**: 1

Hash-based consistent instance selection.

[TIP] **Suggested split**: Move to `hashselector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
