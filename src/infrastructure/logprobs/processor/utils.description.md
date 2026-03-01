# utils

**File**: `src\infrastructure\logprobs\processor\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 4 imports  
**Lines**: 36  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for utils.

## Functions (3)

### `compute_perplexity(logprobs)`

Compute perplexity from logprobs.

### `compute_entropy(logprobs)`

Compute entropy from logprobs (assuming they're top-k).

### `normalize_logprobs(logprobs, axis)`

Normalize logprobs to sum to 1 (in log space).

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `math`
- `numpy`
- `typing.Sequence`

---
*Auto-generated documentation*
