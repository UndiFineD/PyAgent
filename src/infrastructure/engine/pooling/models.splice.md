# Class Breakdown: models

**File**: `src\infrastructure\engine\pooling\models.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PoolingTask`

**Line**: 30  
**Inherits**: Enum  
**Methods**: 0

Supported pooling tasks.

[TIP] **Suggested split**: Move to `poolingtask.py`

---

### 2. `PoolingStrategy`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Pooling strategies for sequence representations.

[TIP] **Suggested split**: Move to `poolingstrategy.py`

---

### 3. `PoolingConfig`

**Line**: 57  
**Methods**: 1

Configuration for pooling operations.

[TIP] **Suggested split**: Move to `poolingconfig.py`

---

### 4. `PoolingResult`

**Line**: 84  
**Methods**: 3

Result from pooling operation.

[TIP] **Suggested split**: Move to `poolingresult.py`

---

### 5. `EmbeddingOutput`

**Line**: 110  
**Methods**: 1

Output for embedding tasks.

[TIP] **Suggested split**: Move to `embeddingoutput.py`

---

### 6. `ClassificationOutput`

**Line**: 123  
**Methods**: 0

Output for classification tasks.

[TIP] **Suggested split**: Move to `classificationoutput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
