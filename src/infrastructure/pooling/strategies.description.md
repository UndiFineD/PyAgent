# strategies

**File**: `src\infrastructure\pooling\strategies.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 8 imports  
**Lines**: 263  
**Complexity**: 21 (complex)

## Overview

Strategy-based poolers for sequence representations.

## Classes (10)

### `BasePooler`

**Inherits from**: ABC

Abstract base for pooling operations.

**Methods** (5):
- `__init__(self, config)`
- `pool_and_process(self, hidden_states, attention_mask)`
- `pool(self, hidden_states, attention_mask)`
- `normalize(self, embeddings)`
- `truncate(self, embeddings, dim)`

### `MeanPooler`

**Inherits from**: BasePooler

Mean pooling over sequence.

**Methods** (1):
- `pool(self, hidden_states, attention_mask)`

### `CLSPooler`

**Inherits from**: BasePooler

First token ([CLS]) pooling.

**Methods** (1):
- `pool(self, hidden_states, attention_mask)`

### `LastTokenPooler`

**Inherits from**: BasePooler

Last token pooling.

**Methods** (1):
- `pool(self, hidden_states, attention_mask)`

### `MaxPooler`

**Inherits from**: BasePooler

Max pooling over sequence.

**Methods** (1):
- `pool(self, hidden_states, attention_mask)`

### `AttentionPooler`

**Inherits from**: BasePooler

Attention-weighted pooling.

**Methods** (2):
- `__init__(self, config, hidden_dim)`
- `pool(self, hidden_states, attention_mask)`

### `WeightedMeanPooler`

**Inherits from**: BasePooler

IDF-weighted mean pooling.

**Methods** (2):
- `__init__(self, config, token_weights)`
- `pool(self, hidden_states, attention_mask, token_ids)`

### `MatryoshkaPooler`

**Inherits from**: BasePooler

Matryoshka Representation Learning (MRL) pooler.
Allows for truncate-able embeddings.

**Methods** (3):
- `__init__(self, config, supported_dims)`
- `pool(self, hidden_states, attention_mask)`
- `get_dimension(self, dim)`

### `MultiVectorPooler`

**Inherits from**: BasePooler

Pooler that preserves multiple vectors per sequence (e.g., ColBERT style).

**Methods** (3):
- `__init__(self, config, compression_dim)`
- `pool(self, hidden_states, attention_mask)`
- `maxsim_score(self, query_vectors, doc_vectors)`

### `StepPooler`

**Inherits from**: BasePooler

Pooler that extracts specific 'step' tokens (e.g., for Chain of Thought).

**Methods** (2):
- `__init__(self, config, step_token_ids)`
- `pool(self, hidden_states, attention_mask, token_ids)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `math`
- `models.PoolingConfig`
- `numpy`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
