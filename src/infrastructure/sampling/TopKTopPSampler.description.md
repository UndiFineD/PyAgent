# TopKTopPSampler

**File**: `src\infrastructure\sampling\TopKTopPSampler.py`  
**Type**: Python Module  
**Summary**: 9 classes, 2 functions, 14 imports  
**Lines**: 655  
**Complexity**: 27 (complex)

## Overview

Top-K and Top-P (Nucleus) Sampling Implementation.

This module provides platform-optimized sampling with support for:
- Multiple backends (NumPy, PyTorch, FlashInfer, aiter)
- Temperature scheduling (constant, linear, cosine, adaptive)
- Nucleus variants (standard, typical, eta, epsilon)
- Combined top-k + top-p filtering

Beyond vLLM innovations:
- Unified multi-backend interface
- Temperature scheduling strategies
- Typical/Eta/Epsilon sampling variants
- Batch-optimized operations
- Min-P filtering support

## Classes (9)

### `SamplingBackend`

**Inherits from**: Enum

Available sampling backends.

### `NucleusSamplingVariant`

**Inherits from**: Enum

Nucleus sampling variants.

### `TemperatureSchedule`

**Inherits from**: Enum

Temperature scheduling strategies.

### `SamplingConfig`

Configuration for top-k/top-p sampling.

**Methods** (1):
- `__post_init__(self)`

### `SamplingState`

Mutable state for temperature scheduling.

**Methods** (3):
- `update_step(self)`
- `add_entropy(self, entropy)`
- `reset(self)`

### `BaseSampler`

**Inherits from**: ABC

Abstract base class for samplers.

**Methods** (3):
- `sample(self, logits, config)`
- `apply_top_k(self, logits, k)`
- `apply_top_p(self, logits, p)`

### `TopKTopPSampler`

Unified Top-K/Top-P sampler with platform optimizations.

Implements vLLM's sampling with additional features:
- Temperature scheduling
- Nucleus variants (typical, eta, epsilon)
- Min-P filtering
- Multi-backend support

**Methods** (14):
- `__init__(self, config)`
- `sample(self, logits, temperature, top_k, top_p)`
- `_apply_filters(self, logits, k, p)`
- `_apply_top_k(self, logits, k)`
- `_apply_top_p(self, logits, p)`
- `_apply_min_p(self, logits, min_p)`
- `_apply_typical_sampling(self, logits, mass)`
- `_apply_eta_sampling(self, logits, eta)`
- `_apply_epsilon_sampling(self, logits, epsilon)`
- `_sample_numpy(self, logits)`
- ... and 4 more methods

### `BatchTopKTopPSampler`

Batch-optimized top-k/top-p sampler.

Optimized for processing multiple requests with different
sampling parameters efficiently.

**Methods** (2):
- `__init__(self)`
- `sample_batch(self, logits, temperatures, top_ks, top_ps)`

### `GumbelSoftmaxSampler`

Gumbel-Softmax sampler for differentiable sampling.

Beyond vLLM: Supports differentiable sampling for gradient-based
optimization scenarios.

**Methods** (2):
- `__init__(self, temperature, hard)`
- `sample(self, logits)`

## Functions (2)

### `create_sampler(backend, variant, temperature_schedule)`

Factory function to create sampler with specified configuration.

Args:
    backend: "numpy", "pytorch", "flashinfer", "aiter", "rust"
    variant: "standard", "typical", "eta", "epsilon", "min_p"
    temperature_schedule: "constant", "linear", "cosine", "adaptive"
    **kwargs: Additional SamplingConfig parameters

### `apply_top_k_top_p(logits, k, p)`

Convenience function to apply top-k and/or top-p filtering.

Args:
    logits: Input logits [batch, vocab] or [vocab]
    k: Top-k value (None or 0 = disabled)
    p: Top-p value (None or 1.0 = disabled)
    
Returns:
    Filtered logits

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `numpy.typing.NDArray`
- `rust_core`
- `typing.Any`
- `typing.Callable`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
