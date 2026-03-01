# NgramProposer

**File**: `src\infrastructure\speculative_v2\NgramProposer.py`  
**Type**: Python Module  
**Summary**: 9 classes, 0 functions, 9 imports  
**Lines**: 572  
**Complexity**: 26 (complex)

## Overview

NgramProposer: N-gram Based Speculative Decoding

Implements prompt-lookup and n-gram based draft token proposal
with Numba-accelerated batch processing for high throughput.

Key Features Beyond vLLM:
- Multi-threading with adaptive thread count
- Fuzzy n-gram matching
- Weighted scoring by recency and frequency
- Streaming prompt integration
- Per-request n-gram caches

Based on vLLM v1 patterns with PyAgent innovations.

## Classes (9)

### `NgramConfig`

Configuration for N-gram proposer.

### `NgramMatch`

Represents an n-gram match in the context.

### `NgramProposalResult`

Result of n-gram proposal.

### `NgramCache`

Cache for n-gram lookups with position tracking.

Stores n-grams with their positions for fast lookup.

**Methods** (5):
- `__init__(self, max_n, max_entries)`
- `add(self, tokens, position)`
- `lookup(self, prefix)`
- `_evict_oldest(self)`
- `clear(self)`

### `NgramProposer`

N-gram based speculative decoding proposer.

Uses prompt lookup to find matching n-grams and propose
following tokens as draft candidates.

**Methods** (11):
- `__init__(self, config)`
- `propose(self, token_ids, request_id, excluded_tokens)`
- `_find_match(self, context, prefix, excluded)`
- `_compute_score(self, position, context_len)`
- `batch_propose(self, batch_token_ids, batch_request_ids)`
- `_batch_propose_sequential(self, batch_token_ids, batch_request_ids)`
- `_batch_propose_parallel(self, batch_token_ids, batch_request_ids)`
- `propose_fuzzy(self, token_ids, max_distance)`
- `_hamming_distance(self, a, b)`
- `get_cache(self, request_id)`
- ... and 1 more methods

### `WeightedNgramProposer`

**Inherits from**: NgramProposer

N-gram proposer with frequency and recency weighting.

Tracks n-gram occurrences and weights matches by frequency.

**Methods** (3):
- `__init__(self, config, decay_factor)`
- `update_stats(self, token_ids)`
- `_compute_score(self, position, context_len)`

### `PromptLookupProposer`

Prompt-lookup based proposer that searches for repetitions.

Specialized for scenarios where the prompt contains repetitive patterns
that are likely to continue in generation.

**Methods** (2):
- `__init__(self, min_lookup_len, max_lookup_len, num_speculative_tokens)`
- `propose(self, prompt_tokens, generated_tokens)`

### `HybridNgramProposer`

Hybrid proposer combining exact and fuzzy n-gram matching.

Falls back to fuzzy matching when exact matching fails.

**Methods** (2):
- `__init__(self, config)`
- `propose(self, token_ids, prompt_len, use_fuzzy)`

### `NgramProposerFactory`

Factory for creating N-gram proposers.

**Methods** (3):
- `create_simple(num_speculative_tokens, min_n, max_n)`
- `create_weighted(num_speculative_tokens, decay_factor)`
- `create_hybrid(num_speculative_tokens, min_n, max_n)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `math`
- `rust_core`
- `threading`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
