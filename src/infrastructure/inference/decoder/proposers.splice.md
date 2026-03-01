# Class Breakdown: proposers

**File**: `src\infrastructure\inference\decoder\proposers.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DraftProposer`

**Line**: 10  
**Inherits**: Protocol  
**Methods**: 2

Protocol for draft token proposers.

[TIP] **Suggested split**: Move to `draftproposer.py`

---

### 2. `NgramProposer`

**Line**: 31  
**Methods**: 6

N-gram based draft proposer.

Matches patterns from the prompt to propose likely continuations.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 3. `SuffixNode`

**Line**: 125  
**Methods**: 1

Node in a suffix tree.

[TIP] **Suggested split**: Move to `suffixnode.py`

---

### 4. `SuffixProposer`

**Line**: 136  
**Methods**: 8

Suffix tree based draft proposer.

Builds a suffix tree from past generations and uses frequency
counts to propose likely continuations.

[TIP] **Suggested split**: Move to `suffixproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
