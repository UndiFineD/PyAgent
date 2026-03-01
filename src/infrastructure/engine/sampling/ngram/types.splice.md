# Class Breakdown: types

**File**: `src\infrastructure\engine\sampling\ngram\types.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MatchingStrategy`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Strategy regarding n-gram matching.

[TIP] **Suggested split**: Move to `matchingstrategy.py`

---

### 2. `NgramConfig`

**Line**: 46  
**Methods**: 1

Configuration regarding n-gram proposer.

[TIP] **Suggested split**: Move to `ngramconfig.py`

---

### 3. `ProposalStats`

**Line**: 70  
**Methods**: 3

Statistics regarding n-gram proposals.

[TIP] **Suggested split**: Move to `proposalstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
