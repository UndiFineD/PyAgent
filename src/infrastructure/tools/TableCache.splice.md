# Class Breakdown: TableCache

**File**: `src\infrastructure\tools\TableCache.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TableMetadata`

**Line**: 11  
**Methods**: 0

[TIP] **Suggested split**: Move to `tablemetadata.py`

---

### 2. `TableTrieNode`

**Line**: 16  
**Methods**: 1

[TIP] **Suggested split**: Move to `tabletrienode.py`

---

### 3. `TableCacheManager`

**Line**: 21  
**Methods**: 5

Manages a Trie-based cache of database schema metadata.
Enables 3.6x TTFT speedup for Text-to-SQL tasks by pre-filtering schema.

[TIP] **Suggested split**: Move to `tablecachemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
