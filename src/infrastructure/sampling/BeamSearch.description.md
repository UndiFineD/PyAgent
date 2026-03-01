# BeamSearch

**File**: `src\infrastructure\sampling\BeamSearch.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 114  
**Complexity**: 10 (moderate)

## Overview

Beam search implementation.

## Classes (3)

### `BeamSearchConfig`

Configuration for beam search.

### `BeamHypothesis`

A hypothesis in beam search.

**Methods** (4):
- `length(self)`
- `normalized_score(self, length_penalty)`
- `extend(self, token_id, log_prob)`
- `finish(self)`

### `BeamSearchSampler`

**Inherits from**: Sampler

Beam search sampler.

**Methods** (6):
- `__init__(self, config)`
- `reset(self)`
- `forward(self, logits, params, state)`
- `step(self, logits, eos_token_id)`
- `get_best_hypothesis(self)`
- `is_finished(self)`

## Dependencies

**Imports** (13):
- `Base.HAS_RUST`
- `Base.Sampler`
- `Base._log_softmax`
- `Params.SamplingParams`
- `Params.SamplingState`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `rust_core.beam_score_rust`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
