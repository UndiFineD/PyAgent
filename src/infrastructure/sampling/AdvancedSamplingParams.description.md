# AdvancedSamplingParams

**File**: `src\infrastructure\sampling\AdvancedSamplingParams.py`  
**Type**: Python Module  
**Summary**: 10 classes, 2 functions, 15 imports  
**Lines**: 593  
**Complexity**: 23 (complex)

## Overview

AdvancedSamplingParams: Extended sampling with vLLM parity and beyond.

Provides:
- Bad words blocking (token sequence filtering)
- Flat logprobs format (GC-optimized)
- Allowed token whitelist
- Per-request cache bypass
- Dynamic temperature scheduling
- Adaptive top-k/top-p based on entropy

## Classes (10)

### `OutputKind`

**Inherits from**: Enum

How to return generation output.

### `StopCondition`

**Inherits from**: Enum

Stop generation conditions.

### `TemperatureSchedule`

**Inherits from**: Enum

Temperature scheduling strategies.

### `SamplingParams`

Base sampling parameters with vLLM parity.

Matches vLLM's sampling_params.py for compatibility.

**Methods** (1):
- `__post_init__(self)`

### `AdvancedSamplingParams`

**Inherits from**: SamplingParams

Extended sampling parameters beyond vLLM.

Features:
- Bad words blocking
- Flat logprobs format
- Allowed token whitelist
- Dynamic temperature scheduling
- Adaptive sampling based on entropy
- Contextual repetition penalty

**Methods** (3):
- `get_temperature(self, step)`
- `get_adaptive_top_k(self, entropy)`
- `get_contextual_penalty(self, distance)`

### `LogitBiasBuilder`

Builder for complex logit bias configurations.

**Methods** (6):
- `__init__(self)`
- `add_bias(self, token_id, bias)`
- `ban_token(self, token_id)`
- `prefer_token(self, token_id, strength)`
- `from_dict(self, biases)`
- `build(self)`

### `BadWordsProcessor`

Processes bad words to block during generation.

Supports:
- String-based bad words (requires tokenizer)
- Token ID sequences
- Dynamic blocking based on context

**Methods** (3):
- `__init__(self, bad_words, bad_words_ids, tokenizer)`
- `get_banned_tokens(self, context_ids)`
- `apply_to_logits(self, logits, context_ids)`

### `TokenWhitelistProcessor`

Restricts generation to allowed tokens only.

Useful for constrained generation (e.g., JSON, code).

**Methods** (3):
- `__init__(self, allowed_token_ids)`
- `build_mask(self, vocab_size)`
- `apply_to_logits(self, logits, vocab_size)`

### `MirostatSampler`

Mirostat sampling for controlled perplexity.

Ref: https://arxiv.org/abs/2007.14966

**Methods** (2):
- `__init__(self, tau, eta, mode)`
- `sample(self, logits)`

### `SamplingEngine`

Unified sampling engine with all advanced features.

Combines:
- Temperature/top-k/top-p sampling
- Bad words blocking
- Token whitelisting
- Mirostat sampling
- Adaptive sampling

**Methods** (3):
- `__init__(self, params)`
- `sample(self, logits, context_ids)`
- `reset(self)`

## Functions (2)

### `create_sampling_params(temperature, top_p, top_k, max_tokens)`

Create basic sampling parameters.

### `create_advanced_sampling_params(temperature, top_p, top_k, max_tokens, adaptive)`

Create advanced sampling parameters.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
