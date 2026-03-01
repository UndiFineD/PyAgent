# engine

**File**: `src\infrastructure\pooling\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 21 imports  
**Lines**: 115  
**Complexity**: 5 (moderate)

## Overview

Core Pooling Engine implementation.

## Classes (1)

### `PoolingEngine`

Manager for various pooling operations.

**Methods** (4):
- `__init__(self, config)`
- `get_pooler(self, strategy)`
- `pool(self, hidden_states, attention_mask, strategy, normalize, truncate_dim)`
- `_ensure_numpy(self, data)`

## Functions (1)

### `create_pooling_engine(config)`

Factory function for PoolingEngine.

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `logging`
- `models.PoolingConfig`
- `models.PoolingResult`
- `models.PoolingStrategy`
- `numpy`
- `strategies.AttentionPooler`
- `strategies.BasePooler`
- `strategies.CLSPooler`
- `strategies.LastTokenPooler`
- `strategies.MatryoshkaPooler`
- `strategies.MaxPooler`
- `strategies.MeanPooler`
- `strategies.MultiVectorPooler`
- `strategies.StepPooler`
- ... and 6 more

---
*Auto-generated documentation*
