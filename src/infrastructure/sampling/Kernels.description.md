# Kernels

**File**: `src\infrastructure\sampling\Kernels.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 12 imports  
**Lines**: 216  
**Complexity**: 8 (moderate)

## Overview

Core sampling kernels and strategies.

## Classes (7)

### `TemperatureSampler`

**Inherits from**: Sampler

Temperature scaling sampler.

**Methods** (1):
- `forward(self, logits, params, state)`

### `TopKSampler`

**Inherits from**: Sampler

Top-K filtering sampler.

**Methods** (1):
- `forward(self, logits, params, state)`

### `TopPSampler`

**Inherits from**: Sampler

Top-P (nucleus) sampling.

**Methods** (1):
- `forward(self, logits, params, state)`

### `TopKTopPSampler`

**Inherits from**: Sampler

Combined top-k and top-p filtering.

**Methods** (1):
- `forward(self, logits, params, state)`

### `GumbelSampler`

**Inherits from**: Sampler

Gumbel-max trick sampler.

**Methods** (2):
- `forward(self, logits, params, state)`
- `sample(self, logits, params, state)`

### `RepetitionPenaltySampler`

**Inherits from**: Sampler

Repetition penalty sampler.

**Methods** (1):
- `forward(self, logits, params, state)`

### `PenaltySampler`

**Inherits from**: Sampler

Presence and frequency penalty sampler.

**Methods** (1):
- `forward(self, logits, params, state)`

## Dependencies

**Imports** (12):
- `Base.HAS_RUST`
- `Base.Sampler`
- `Base._softmax`
- `Params.SamplingParams`
- `Params.SamplingState`
- `__future__.annotations`
- `numpy`
- `rust_core.compute_penalties_rust`
- `rust_core.gumbel_sample_rust`
- `rust_core.top_k_mask_rust`
- `rust_core.top_p_mask_rust`
- `typing.Optional`

---
*Auto-generated documentation*
