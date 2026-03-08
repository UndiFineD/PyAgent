# Class Breakdown: automem_core

**File**: `src\core\memory\automem_core.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemoryConfig`

**Line**: 112  
**Methods**: 0

Configuration for AutoMem memory system.

[TIP] **Suggested split**: Move to `memoryconfig.py`

---

### 2. `Memory`

**Line**: 125  
**Methods**: 0

Represents a single memory with metadata.

[TIP] **Suggested split**: Move to `memory.py`

---

### 3. `AutoMemCore`

**Line**: 138  
**Methods**: 16

AutoMem Memory System Core.

Implements graph-vector hybrid memory with FalkorDB + Qdrant.
Based on the world's highest-performing memory system (90.53% LoCoMo benchmark).

[TIP] **Suggested split**: Move to `automemcore.py`

---

### 4. `MemoryConsolidator`

**Line**: 519  
**Methods**: 9

Memory consolidation system with neuroscience-inspired cycles.

Implements decay, creative, cluster, and forget consolidation types.

[TIP] **Suggested split**: Move to `memoryconsolidator.py`

---

### 5. `PointStruct`

**Line**: 69  
**Methods**: 1

[TIP] **Suggested split**: Move to `pointstruct.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
