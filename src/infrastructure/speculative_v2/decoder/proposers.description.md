# proposers

**File**: `src\infrastructure\speculative_v2\decoder\proposers.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 11 imports  
**Lines**: 191  
**Complexity**: 16 (moderate)

## Overview

Implementations of speculative token proposers.

## Classes (4)

### `ProposerStats`

Statistics for a proposer.

**Methods** (2):
- `acceptance_rate(self)`
- `avg_proposal_time_ms(self)`

### `SpeculativeProposer`

**Inherits from**: ABC

Abstract base class for speculative token proposers.

**Methods** (5):
- `__init__(self, vocab_size, max_speculation_depth)`
- `propose(self, input_ids, attention_mask, num_candidates)`
- `update(self, accepted_tokens, rejected_at)`
- `get_stats(self)`
- `reset_stats(self)`

### `NgramProposer`

**Inherits from**: SpeculativeProposer

N-gram based speculative proposer.

**Methods** (5):
- `__init__(self, vocab_size, max_speculation_depth, ngram_order, min_count)`
- `_update_ngrams(self, tokens)`
- `_get_predictions(self, context, top_k)`
- `propose(self, input_ids, attention_mask, num_candidates)`
- `update(self, accepted_tokens, rejected_at)`

### `MedusaProposer`

**Inherits from**: SpeculativeProposer

Medusa-style multi-head prediction proposer.

**Methods** (4):
- `__init__(self, vocab_size, max_speculation_depth, num_heads, top_k_per_head)`
- `_sample_from_head(self, head_idx, top_k)`
- `propose(self, input_ids, attention_mask, num_candidates)`
- `update(self, accepted_tokens, rejected_at)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `numpy`
- `time`
- `tree.SpeculativeTree`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
