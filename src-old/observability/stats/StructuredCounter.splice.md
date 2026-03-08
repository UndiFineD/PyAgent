# Class Breakdown: StructuredCounter

**File**: `src\observability\stats\StructuredCounter.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StructuredCounter`

**Line**: 21  
**Methods**: 7

Base class for structured metric counters.

Provides snapshot, diff, and testing utilities for tracking
detailed metrics across operations.

Usage:
    @dataclass
    class MyCounter(StructuredCounter...

[TIP] **Suggested split**: Move to `structuredcounter.py`

---

### 2. `CompilationCounter`

**Line**: 119  
**Inherits**: StructuredCounter  
**Methods**: 0

Counter for tracking compilation-related metrics.

Based on vLLM's compilation counter pattern.

[TIP] **Suggested split**: Move to `compilationcounter.py`

---

### 3. `RequestCounter`

**Line**: 135  
**Inherits**: StructuredCounter  
**Methods**: 0

Counter for tracking request-related metrics.

[TIP] **Suggested split**: Move to `requestcounter.py`

---

### 4. `CacheCounter`

**Line**: 147  
**Inherits**: StructuredCounter  
**Methods**: 1

Counter for tracking cache-related metrics.

[TIP] **Suggested split**: Move to `cachecounter.py`

---

### 5. `PoolCounter`

**Line**: 163  
**Inherits**: StructuredCounter  
**Methods**: 1

Counter for tracking object pool metrics.

[TIP] **Suggested split**: Move to `poolcounter.py`

---

### 6. `QueueCounter`

**Line**: 179  
**Inherits**: StructuredCounter  
**Methods**: 0

Counter for tracking queue metrics.

[TIP] **Suggested split**: Move to `queuecounter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
