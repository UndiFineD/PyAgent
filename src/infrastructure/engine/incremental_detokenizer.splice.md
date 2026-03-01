# Class Breakdown: incremental_detokenizer

**File**: `src\infrastructure\engine\incremental_detokenizer.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StopMatch`

**Line**: 42  
**Methods**: 0

Result of stop string matching.

[TIP] **Suggested split**: Move to `stopmatch.py`

---

### 2. `IncrementalDetokenizer`

**Line**: 106  
**Inherits**: ABC  
**Methods**: 5

Base class for incremental detokenization.

Converts token IDs to text incrementally, handling special tokens
and stop strings efficiently.

[TIP] **Suggested split**: Move to `incrementaldetokenizer.py`

---

### 3. `NoOpDetokenizer`

**Line**: 173  
**Inherits**: IncrementalDetokenizer  
**Methods**: 2

No-op detokenizer when tokenizer is not available.

[TIP] **Suggested split**: Move to `noopdetokenizer.py`

---

### 4. `BaseIncrementalDetokenizer`

**Line**: 184  
**Inherits**: IncrementalDetokenizer, ABC  
**Methods**: 7

Base class with common functionality for incremental detokenizers.

[TIP] **Suggested split**: Move to `baseincrementaldetokenizer.py`

---

### 5. `FastIncrementalDetokenizer`

**Line**: 284  
**Inherits**: BaseIncrementalDetokenizer  
**Methods**: 5

Fast incremental detokenizer using tokenizers library's DecodeStream.

Requires tokenizers >= 0.21.1 for DecodeStream support.

[TIP] **Suggested split**: Move to `fastincrementaldetokenizer.py`

---

### 6. `SlowIncrementalDetokenizer`

**Line**: 395  
**Inherits**: BaseIncrementalDetokenizer  
**Methods**: 5

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
