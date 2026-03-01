# Class Breakdown: context_sharder

**File**: `src\infrastructure\engine\kv_cache\context_sharder.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ContextShard`

**Line**: 30  
**Methods**: 0

Metadata for a sharded slice of a long context.

[TIP] **Suggested split**: Move to `contextshard.py`

---

### 2. `ContextShardManager`

**Line**: 45  
**Methods**: 5

Manages distribution of long-context shards across the swarm.
Prevents context replication bottleneck.

[TIP] **Suggested split**: Move to `contextshardmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
