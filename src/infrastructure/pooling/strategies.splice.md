# Class Breakdown: strategies

**File**: `src\infrastructure\pooling\strategies.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BasePooler`

**Line**: 31  
**Inherits**: ABC  
**Methods**: 5

Abstract base for pooling operations.

[TIP] **Suggested split**: Move to `basepooler.py`

---

### 2. `MeanPooler`

**Line**: 71  
**Inherits**: BasePooler  
**Methods**: 1

Mean pooling over sequence.

[TIP] **Suggested split**: Move to `meanpooler.py`

---

### 3. `CLSPooler`

**Line**: 89  
**Inherits**: BasePooler  
**Methods**: 1

First token ([CLS]) pooling.

[TIP] **Suggested split**: Move to `clspooler.py`

---

### 4. `LastTokenPooler`

**Line**: 100  
**Inherits**: BasePooler  
**Methods**: 1

Last token pooling.

[TIP] **Suggested split**: Move to `lasttokenpooler.py`

---

### 5. `MaxPooler`

**Line**: 117  
**Inherits**: BasePooler  
**Methods**: 1

Max pooling over sequence.

[TIP] **Suggested split**: Move to `maxpooler.py`

---

### 6. `AttentionPooler`

**Line**: 133  
**Inherits**: BasePooler  
**Methods**: 2

Attention-weighted pooling.

[TIP] **Suggested split**: Move to `attentionpooler.py`

---

### 7. `WeightedMeanPooler`

**Line**: 156  
**Inherits**: BasePooler  
**Methods**: 2

IDF-weighted mean pooling.

[TIP] **Suggested split**: Move to `weightedmeanpooler.py`

---

### 8. `MatryoshkaPooler`

**Line**: 183  
**Inherits**: BasePooler  
**Methods**: 3

Matryoshka Representation Learning (MRL) pooler.
Allows for truncate-able embeddings.

[TIP] **Suggested split**: Move to `matryoshkapooler.py`

---

### 9. `MultiVectorPooler`

**Line**: 216  
**Inherits**: BasePooler  
**Methods**: 3

Pooler that preserves multiple vectors per sequence (e.g., ColBERT style).

[TIP] **Suggested split**: Move to `multivectorpooler.py`

---

### 10. `StepPooler`

**Line**: 244  
**Inherits**: BasePooler  
**Methods**: 2

Pooler that extracts specific 'step' tokens (e.g., for Chain of Thought).

[TIP] **Suggested split**: Move to `steppooler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
