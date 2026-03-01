# Engine

**File**: `src\infrastructure\sampling\Engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 14 imports  
**Lines**: 72  
**Complexity**: 5 (moderate)

## Overview

Execution engine for the sampling pipeline.

## Classes (1)

### `SamplingPipeline`

Composable pipeline of samplers.

**Methods** (4):
- `__init__(self, samplers)`
- `add_sampler(self, sampler)`
- `forward(self, logits, params, state)`
- `sample(self, logits, params, state)`

## Functions (1)

### `sample_logits(logits, params, state)`

Convenience function to sample from logits.

## Dependencies

**Imports** (14):
- `Base.Sampler`
- `Base._sample_from_probs`
- `Base._softmax`
- `Kernels.GumbelSampler`
- `Kernels.PenaltySampler`
- `Kernels.RepetitionPenaltySampler`
- `Kernels.TemperatureSampler`
- `Kernels.TopKTopPSampler`
- `Params.SamplingParams`
- `Params.SamplingState`
- `__future__.annotations`
- `numpy`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
