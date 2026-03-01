# Params

**File**: `src\infrastructure\sampling\Params.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 120  
**Complexity**: 9 (moderate)

## Overview

Sampling parameters and state tracking.

## Classes (2)

### `SamplingParams`

Parameters for controlling text generation sampling.

Attributes:
    temperature: Temperature for softmax. Higher = more random.
    top_k: Number of top tokens to consider. -1 or 0 = disabled.
    top_p: Cumulative probability threshold (nucleus sampling).
    min_p: Minimum probability relative to top token.
    repetition_penalty: Penalty for repeated tokens (> 1.0).
    presence_penalty: Additive penalty for presence of tokens.
    frequency_penalty: Additive penalty based on frequency.
    seed: Random seed for reproducibility.
    max_tokens: Maximum tokens to generate.
    min_tokens: Minimum tokens to generate before stopping.
    stop_token_ids: Token IDs that trigger stopping.
    ignore_eos: Whether to ignore EOS token.
    logprobs: Number of top logprobs to return per token.

**Methods** (5):
- `__post_init__(self)`
- `use_temperature(self)`
- `use_top_k(self)`
- `use_top_p(self)`
- `use_min_p(self)`

### `SamplingState`

Per-request state for sampling.

Tracks generated tokens and other stateful information needed
for penalties and constraints.

Attributes:
    request_id: Unique request identifier
    generated_ids: List of generated token IDs
    token_counts: Count of each token ID generated (for frequency penalty)
    prompt_token_ids: Original prompt token IDs (optional)

**Methods** (4):
- `__post_init__(self)`
- `add_token(self, token_id)`
- `get_all_token_ids(self)`
- `from_seed(cls, request_id, seed)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
