# Class Breakdown: IncrementalDetokenizer

**File**: `src\infrastructure\engine\IncrementalDetokenizer.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StopMatch`

**Line**: 23  
**Methods**: 0

Result of stop string matching.

[TIP] **Suggested split**: Move to `stopmatch.py`

---

### 2. `IncrementalDetokenizer`

**Line**: 85  
**Inherits**: ABC  
**Methods**: 5

Base class for incremental detokenization.

Converts token IDs to text incrementally, handling special tokens
and stop strings efficiently.

[TIP] **Suggested split**: Move to `incrementaldetokenizer.py`

---

### 3. `NoOpDetokenizer`

**Line**: 152  
**Inherits**: IncrementalDetokenizer  
**Methods**: 2

No-op detokenizer when tokenizer is not available.

[TIP] **Suggested split**: Move to `noopdetokenizer.py`

---

### 4. `BaseIncrementalDetokenizer`

**Line**: 163  
**Inherits**: IncrementalDetokenizer, ABC  
**Methods**: 4

Base class with common functionality for incremental detokenizers.

[TIP] **Suggested split**: Move to `baseincrementaldetokenizer.py`

---

### 5. `FastIncrementalDetokenizer`

**Line**: 252  
**Inherits**: BaseIncrementalDetokenizer  
**Methods**: 3

Fast incremental detokenizer using tokenizers library's DecodeStream.

Requires tokenizers >= 0.21.1 for DecodeStream support.

[TIP] **Suggested split**: Move to `fastincrementaldetokenizer.py`

---

### 6. `SlowIncrementalDetokenizer`

**Line**: 359  
**Inherits**: BaseIncrementalDetokenizer  
**Methods**: 3

Slow incremental detokenizer using Python-based approach.

Compatible with all tokenizers but slower than FastIncrementalDetokenizer.

[TIP] **Suggested split**: Move to `slowincrementaldetokenizer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
