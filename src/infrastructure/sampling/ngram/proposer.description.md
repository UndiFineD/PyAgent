# proposer

**File**: `src\infrastructure\sampling\ngram\proposer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 280  
**Complexity**: 12 (moderate)

## Overview

N-gram Proposers - Implementation of speculative decoding token proposers.

## Classes (2)

### `NgramProposer`

N-gram based speculative token proposer.

Uses n-gram matching on prompt/context to propose
likely continuations without running a draft model.

**Methods** (9):
- `__init__(self, config)`
- `propose(self, tokens, num_proposals)`
- `_find_matches_linear(self, tokens, ngram)`
- `_get_continuation(self, tokens, position, k)`
- `_score_match(self, proposal, position, total_length, ngram_size)`
- `batch_propose(self, batch_tokens, num_proposals)`
- `get_stats(self)`
- `reset_stats(self)`
- `clear_cache(self)`

### `AdaptiveNgramProposer`

**Inherits from**: NgramProposer

Adaptive n-gram proposer that adjusts parameters based on performance.

**Methods** (3):
- `__init__(self, config)`
- `propose(self, tokens, num_proposals)`
- `update_acceptance(self, acceptance_rate)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `logging`
- `numpy`
- `numpy.typing.NDArray`
- `rust_core`
- `src.infrastructure.sampling.ngram.accelerators.HAS_RUST`
- `src.infrastructure.sampling.ngram.index.SuffixIndex`
- `src.infrastructure.sampling.ngram.types.MatchingStrategy`
- `src.infrastructure.sampling.ngram.types.NgramConfig`
- `src.infrastructure.sampling.ngram.types.ProposalStats`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
