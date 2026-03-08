# Class Breakdown: ProfilingCore

**File**: `src\observability\stats\core\ProfilingCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProfileStats`

**Line**: 8  
**Methods**: 0

[TIP] **Suggested split**: Move to `profilestats.py`

---

### 2. `ProfilingCore`

**Line**: 14  
**Methods**: 3

Pure logic for cProfile aggregation and bottleneck analysis.
Identifies slow methods and calculates optimization priority.

[TIP] **Suggested split**: Move to `profilingcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
