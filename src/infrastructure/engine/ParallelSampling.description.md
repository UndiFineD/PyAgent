# ParallelSampling

**File**: `src\infrastructure\engine\ParallelSampling.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 14 imports  
**Lines**: 633  
**Complexity**: 35 (complex)

## Overview

Parallel Sampling - Multi-sample request handling (n > 1).

Implements vLLM's ParallelSampling patterns with PyAgent enhancements:
- Parent/child request management
- Output aggregation for n > 1 sampling
- Seed distribution for reproducibility
- Statistics tracking across samples

Beyond vLLM:
- Beam search integration
- Best-of-n filtering
- Diverse sampling strategies
- Sample quality scoring

## Classes (11)

### `SamplingStrategy`

**Inherits from**: Enum

Strategy for generating multiple samples.

### `OutputKind`

**Inherits from**: Enum

Kind of output to return.

### `SamplingParams`

Parameters for sampling.

**Methods** (1):
- `requires_parallel_sampling(self)`

### `CompletionOutput`

Output for a single completion.

**Methods** (3):
- `finished(self)`
- `append(self, token_id, text, logprob)`
- `compute_score(self)`

### `ParentRequest`

Parent request managing multiple child samples.

For n > 1 sampling, creates n child requests and
aggregates their outputs.

**Methods** (8):
- `__post_init__(self)`
- `n(self)`
- `best_of(self)`
- `get_child_info(self, index)`
- `_get_child_sampling_params(self, index)`
- `record_child_output(self, child_request_id, completion)`
- `_get_final_outputs(self)`
- `all_finished(self)`

### `ParallelSamplingManager`

Manages parallel sampling across multiple parent requests.

Features:
- Parent/child request mapping
- Output aggregation
- Statistics tracking

**Methods** (6):
- `create_parent(self, request_id, sampling_params)`
- `get_child_requests(self, parent)`
- `record_output(self, request_id, completion)`
- `finish_parent(self, parent_id)`
- `get_parent(self, request_id)`
- `is_child_request(self, request_id)`

### `BeamState`

State for beam search.

**Methods** (1):
- `extend(self, token_id, logprob)`

### `BeamSearchManager`

Beam search implementation.

Maintains top-k beams during generation.

**Methods** (5):
- `__init__(self, beam_width, length_penalty, early_stopping)`
- `init_request(self, request_id)`
- `update_beams(self, request_id, token_scores)`
- `mark_finished(self, request_id, beam_idx)`
- `get_best_sequences(self, request_id, n)`

### `DiverseSamplingManager`

Diverse sampling to maximize output variety.

Uses hamming distance penalty to encourage diverse outputs.

**Methods** (4):
- `__init__(self, diversity_penalty, group_size)`
- `init_request(self, request_id, n)`
- `compute_diversity_penalty(self, request_id, sample_idx, token_id)`
- `record_token(self, request_id, sample_idx, token_id)`

### `BestOfNFilter`

Filter to select best outputs from n samples.

Uses various scoring metrics beyond log probability.

**Methods** (3):
- `__init__(self, score_fn)`
- `_default_score(self, output)`
- `select_best(self, outputs, n)`

### `IterationStats`

Statistics for a single iteration/step.

**Methods** (4):
- `record_finished_request(self, e2e_latency, num_prompt_tokens, num_generation_tokens, finish_reason, num_cached_tokens)`
- `record_first_token(self, latency)`
- `record_inter_token_latency(self, latency)`
- `observe_parallel_sampling(self, parent, num_generation_tokens)`

## Dependencies

**Imports** (14):
- `copy.copy`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
