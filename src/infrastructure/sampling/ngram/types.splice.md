# Class Breakdown: types

**File**: `src\infrastructure\sampling\ngram\types.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MatchingStrategy`

**Line**: 12  
**Inherits**: Enum  
**Methods**: 0

Strategy for n-gram matching.

[TIP] **Suggested split**: Move to `matchingstrategy.py`

---

### 2. `NgramConfig`

**Line**: 21  
**Methods**: 1

Configuration for n-gram proposer.

[TIP] **Suggested split**: Move to `ngramconfig.py`

---

### 3. `ProposalStats`

**Line**: 43  
**Methods**: 3

Statistics for n-gram proposals.

[TIP] **Suggested split**: Move to `proposalstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
