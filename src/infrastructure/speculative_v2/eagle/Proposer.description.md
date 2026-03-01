# Proposer

**File**: `src\infrastructure\speculative_v2\eagle\Proposer.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 16 imports  
**Lines**: 360  
**Complexity**: 15 (moderate)

## Overview

Proposer logic for EAGLE speculative decoding.

## Classes (3)

### `EagleProposer`

EAGLE-style speculative decoding proposer.

**Methods** (12):
- `__init__(self, config, draft_model)`
- `propose(self, input_ids, positions, hidden_states, max_proposals)`
- `_propose_sequential(self, input_ids, positions, hidden_states, num_proposals)`
- `_propose_tree(self, input_ids, positions, hidden_states, num_proposals)`
- `_get_top_k_candidates(self, logits, k)`
- `_get_adaptive_depth(self)`
- `record_acceptance(self, num_proposed, num_accepted)`
- `get_acceptance_rate(self)`
- `build_tree_attention_metadata(self, tree, base_seq_len)`
- `verify_and_accept(self, draft_tokens, draft_logprobs, target_logprobs, sampling_eps)`
- ... and 2 more methods

### `EagleProposerFactory`

Factory for creating EAGLE proposers.

**Methods** (2):
- `create(method, num_speculative_tokens, hidden_size, use_cuda_graph)`
- `create_eagle3(num_speculative_tokens, hidden_size, use_aux_hidden_state)`

### `AsyncEagleProposer`

Async wrapper for EAGLE proposer.

**Methods** (1):
- `__init__(self, proposer)`

## Dependencies

**Imports** (16):
- `Base.TreeAttentionMetadata`
- `Config.EagleConfig`
- `Config.EagleMethod`
- `Models.DraftModelWrapper`
- `Models.DraftOutput`
- `Models.SimpleDraftModel`
- `Stats.AcceptanceStats`
- `Tree.SpeculativeTree`
- `__future__.annotations`
- `asyncio`
- `math`
- `random`
- `rust_core`
- `threading`
- `typing.Any`
- ... and 1 more

---
*Auto-generated documentation*
