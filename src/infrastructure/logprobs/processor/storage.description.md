# storage

**File**: `src\infrastructure\logprobs\processor\storage.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 79  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for storage.

## Classes (1)

### `FlatLogprobs`

GC-optimized flat logprobs storage.

**Methods** (9):
- `__post_init__(self)`
- `num_tokens(self)`
- `top_k(self)`
- `from_entries(cls, entries, top_k)`
- `to_entries(self, tokenizer)`
- `_decode(self, tid, tokenizer)`
- `mean_logprob(self)`
- `perplexity(self)`
- `entropy_per_token(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `config.LogprobEntry`
- `config.TopLogprob`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
