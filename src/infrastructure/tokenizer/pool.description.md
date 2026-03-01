# pool

**File**: `src\infrastructure\tokenizer\pool.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 68  
**Complexity**: 6 (moderate)

## Overview

Tokenizer pool for parallel processing.

## Classes (1)

### `TokenizerPool`

Thread-safe pool of tokenizers.

**Methods** (6):
- `__init__(self, config, pool_size)`
- `_init_pool(self)`
- `acquire(self, timeout)`
- `release(self, tokenizer)`
- `__enter__(self)`
- `__exit__(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `base.BaseTokenizer`
- `models.TokenizerConfig`
- `registry.TokenizerRegistry`
- `threading`
- `time`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
