# Class Breakdown: dimensionality_agent

**File**: `src\logic\agents\specialists\dimensionality_agent.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReductionMethod`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Supported dimensionality reduction methods.

[TIP] **Suggested split**: Move to `reductionmethod.py`

---

### 2. `EmbeddingStats`

**Line**: 64  
**Methods**: 0

Statistics for an embedding.

[TIP] **Suggested split**: Move to `embeddingstats.py`

---

### 3. `DimensionalityAgent`

**Line**: 75  
**Inherits**: BaseAgent  
**Methods**: 3

Agent specializing in simplifying complex datasets and high-dimensional spaces.
Focuses on PCA, t-SNE (simulated), UMAP, and semantic embedding compression.

[TIP] **Suggested split**: Move to `dimensionalityagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
