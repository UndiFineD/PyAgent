# RejectionSampler

**File**: `src\infrastructure\sampling\RejectionSampler.py`  
**Type**: Python Module  
**Summary**: 9 classes, 1 functions, 13 imports  
**Lines**: 660  
**Complexity**: 28 (complex)

## Overview

Rejection Sampler for Speculative Decoding verification.

This module implements the rejection sampling algorithm from the paper:
"Fast Inference from Transformers via Speculative Decoding" (https://arxiv.org/abs/2211.17192)

Features beyond vLLM:
- Multiple rejection strategies (standard, strict, lenient)
- Batch recovery optimization
- Streaming verification mode
- Acceptance probability caching
- Token-level acceptance statistics

## Classes (9)

### `RejectionStrategy`

**Inherits from**: Enum

Rejection strategy determines how strict the acceptance criteria is.

### `RecoveryMode`

**Inherits from**: Enum

How to recover when draft tokens are rejected.

### `RejectionConfig`

Configuration for rejection sampler.

**Methods** (1):
- `__post_init__(self)`

### `AcceptanceStats`

Statistics for rejection sampling.

**Methods** (5):
- `acceptance_rate(self)`
- `position_rates(self)`
- `update(self, accepted, proposed, recovered, bonus)`
- `update_position(self, position, accepted)`
- `reset(self)`

### `RejectionOutput`

Output from rejection sampling.

**Methods** (2):
- `all_tokens(self)`
- `total_tokens(self)`

### `ProbabilityProvider`

**Inherits from**: Protocol

Protocol for providing probability distributions.

**Methods** (2):
- `get_target_probs(self, token_indices)`
- `get_draft_probs(self, token_indices)`

### `RejectionSampler`

Implements rejection sampling for speculative decoding verification.

The algorithm works as follows:
1. For each draft token at position i:
   - Accept with probability min(1, p_target(x) / p_draft(x))
   - If rejected, resample from adjusted distribution: max(0, p_target - p_draft)
2. If all drafts accepted, sample bonus token from target

Beyond vLLM innovations:
- Multiple rejection strategies (strict, lenient, adaptive)
- Batch recovery for efficiency
- Streaming verification for low latency
- Position-aware acceptance statistics

**Methods** (11):
- `__init__(self, config)`
- `verify_and_sample(self, draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)`
- `_verify_python(self, draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)`
- `_compute_acceptance_prob(self, p_target, p_draft)`
- `_resample_from_adjusted(self, target_probs, draft_probs, random_number)`
- `_sample_bonus(self, probs, random_number)`
- `_verify_rust(self, draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)`
- `batch_verify(self, batch_draft_tokens, batch_draft_probs, batch_target_probs, batch_bonus_probs)`
- `get_stats(self)`
- `reset_stats(self)`
- ... and 1 more methods

### `StreamingRejectionSampler`

**Inherits from**: RejectionSampler

Streaming rejection sampler for low-latency verification.

Beyond vLLM: Verifies tokens incrementally as they arrive,
enabling early termination and lower latency.

**Methods** (4):
- `__init__(self, config)`
- `add_token(self, token, draft_prob, target_prob, random_number)`
- `finalize(self, draft_probs, target_probs, bonus_probs)`
- `reset_stream(self)`

### `BatchRejectionSampler`

Optimized batch rejection sampler for high throughput.

Beyond vLLM: Vectorized operations for batch processing,
memory-efficient probability handling, parallel verification.

**Methods** (2):
- `__init__(self, config)`
- `batch_verify_vectorized(self, draft_tokens, draft_probs, target_probs, seq_lens, bonus_probs)`

## Functions (1)

### `create_rejection_sampler(strategy, recovery, streaming, batch_optimized)`

Factory function to create appropriate rejection sampler.

Args:
    strategy: "standard", "strict", "lenient", or "adaptive"
    recovery: "resample", "truncate", or "fallback"
    streaming: Use streaming sampler for low latency
    batch_optimized: Use batch sampler for high throughput
    **kwargs: Additional config options

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `numpy.typing.NDArray`
- `rust_core`
- `typing.Any`
- `typing.Protocol`
- `typing.TYPE_CHECKING`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
