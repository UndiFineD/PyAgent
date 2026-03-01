# Class Breakdown: LocalRAGCore

**File**: `src\logic\agents\cognitive\core\LocalRAGCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RAGShard`

**Line**: 7  
**Methods**: 0

Metadata for a localized vector shard.

[TIP] **Suggested split**: Move to `ragshard.py`

---

### 2. `LocalRAGCore`

**Line**: 14  
**Methods**: 3

Pure logic for hyper-localized RAG and vector sharding.
Handles shard selection, path-based routing, and context relevance.

[TIP] **Suggested split**: Move to `localragcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
