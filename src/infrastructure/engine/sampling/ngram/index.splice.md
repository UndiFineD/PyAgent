# Class Breakdown: index

**File**: `src\infrastructure\engine\sampling\ngram\index.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SuffixIndex`

**Line**: 30  
**Methods**: 6

Suffix-based index regarding fast n-gram lookup.

Beyond vLLM: O(1) average case lookup regarding n-gram matching
using hash-based suffix indexing.

[TIP] **Suggested split**: Move to `suffixindex.py`

---

### 2. `SuffixTreeProposer`

**Line**: 107  
**Methods**: 3

Suffix tree-based proposer regarding O(m) lookup complexity.

Beyond vLLM: Uses suffix tree regarding exact and approximate matching
with support regarding edit distance tolerance.

[TIP] **Suggested split**: Move to `suffixtreeproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
