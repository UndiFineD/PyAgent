# Class Breakdown: index

**File**: `src\infrastructure\sampling\ngram\index.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SuffixIndex`

**Line**: 16  
**Methods**: 6

Suffix-based index for fast n-gram lookup.

Beyond vLLM: O(1) average case lookup for n-gram matching
using hash-based suffix indexing.

[TIP] **Suggested split**: Move to `suffixindex.py`

---

### 2. `SuffixTreeProposer`

**Line**: 94  
**Methods**: 3

Suffix tree-based proposer for O(m) lookup complexity.

Beyond vLLM: Uses suffix tree for exact and approximate matching
with support for edit distance tolerance.

[TIP] **Suggested split**: Move to `suffixtreeproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
