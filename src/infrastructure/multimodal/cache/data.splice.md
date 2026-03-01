# Class Breakdown: data

**File**: `src\infrastructure\multimodal\cache\data.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MediaHash`

**Line**: 12  
**Methods**: 2

Content hash for media items.

[TIP] **Suggested split**: Move to `mediahash.py`

---

### 2. `CacheEntry`

**Line**: 29  
**Methods**: 1

Entry in the multimodal cache.

[TIP] **Suggested split**: Move to `cacheentry.py`

---

### 3. `CacheStats`

**Line**: 47  
**Methods**: 1

Statistics for cache performance.

[TIP] **Suggested split**: Move to `cachestats.py`

---

### 4. `PlaceholderRange`

**Line**: 63  
**Methods**: 1

Range of tokens for multimodal placeholder.

[TIP] **Suggested split**: Move to `placeholderrange.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
