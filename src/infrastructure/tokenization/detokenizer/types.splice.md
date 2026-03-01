# Class Breakdown: types

**File**: `src\infrastructure\tokenization\detokenizer\types.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenizerLike`

**Line**: 20  
**Inherits**: Protocol  
**Methods**: 6

Protocol for tokenizer abstraction.

[TIP] **Suggested split**: Move to `tokenizerlike.py`

---

### 2. `DetokenizeResult`

**Line**: 63  
**Methods**: 1

Result of incremental detokenization.

[TIP] **Suggested split**: Move to `detokenizeresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
