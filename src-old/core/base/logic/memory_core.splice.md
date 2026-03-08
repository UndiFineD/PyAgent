# Class Breakdown: memory_core

**File**: `src\core\base\logic\memory_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemoryNode`

**Line**: 34  
**Methods**: 1

Represents a memory node in the graph

[TIP] **Suggested split**: Move to `memorynode.py`

---

### 2. `MemoryRelation`

**Line**: 53  
**Methods**: 1

Represents a relationship between memory nodes

[TIP] **Suggested split**: Move to `memoryrelation.py`

---

### 3. `MemoryStore`

**Line**: 67  
**Inherits**: ABC  
**Methods**: 0

Abstract base class for memory storage backends

[TIP] **Suggested split**: Move to `memorystore.py`

---

### 4. `GraphMemoryStore`

**Line**: 103  
**Inherits**: MemoryStore  
**Methods**: 1

Graph-based memory store using relationship patterns
Based on AutoMem's FalkorDB patterns

[TIP] **Suggested split**: Move to `graphmemorystore.py`

---

### 5. `VectorMemoryStore`

**Line**: 238  
**Inherits**: MemoryStore  
**Methods**: 2

Vector-based memory store for semantic similarity
Based on AutoMem's Qdrant patterns

[TIP] **Suggested split**: Move to `vectormemorystore.py`

---

### 6. `HybridMemoryCore`

**Line**: 336  
**Methods**: 2

Hybrid graph-vector memory system
Based on AutoMem's dual storage architecture

[TIP] **Suggested split**: Move to `hybridmemorycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
