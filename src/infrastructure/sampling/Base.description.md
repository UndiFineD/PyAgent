# Base

**File**: `src\infrastructure\sampling\Base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 3 functions, 12 imports  
**Lines**: 102  
**Complexity**: 6 (moderate)

## Overview

Base classes and utilities for sampling.

## Classes (1)

### `Sampler`

**Inherits from**: ABC

Abstract base class for sampling strategies.

**Methods** (3):
- `forward(self, logits, params, state)`
- `sample(self, logits, params, state)`
- `_sample_from_logits(self, logits, state)`

## Functions (3)

### `_softmax(logits)`

Numerically stable softmax.

### `_log_softmax(logits)`

Numerically stable log softmax.

### `_sample_from_probs(probs, state)`

Sample token IDs from probability distribution.

## Dependencies

**Imports** (12):
- `Params.SamplingParams`
- `Params.SamplingState`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `numpy`
- `rust_core.beam_score_rust`
- `rust_core.compute_penalties_rust`
- `rust_core.gumbel_sample_rust`
- `rust_core.top_k_mask_rust`
- `rust_core.top_p_mask_rust`
- `typing.Optional`

---
*Auto-generated documentation*
