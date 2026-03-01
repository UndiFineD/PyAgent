# BadWordsProcessorV2

**File**: `src\infrastructure\structured_output\BadWordsProcessorV2.py`  
**Type**: Python Module  
**Summary**: 4 classes, 3 functions, 19 imports  
**Lines**: 411  
**Complexity**: 20 (complex)

## Overview

BadWordsProcessorV2 - Enhanced bad words filtering processor.

Implements vLLM's bad words filtering with:
- N-gram prefix matching
- Speculative decoding support
- Batch-level filtering

Beyond vLLM innovations:
- Trie-based matching for efficiency
- Streaming token support
- Configurable penalty modes
- Bad phrase detection

## Classes (4)

### `BadWordsPenaltyMode`

**Inherits from**: Enum

Penalty mode for bad words.

### `TrieNode`

Trie node for efficient prefix matching.

**Methods** (2):
- `insert(self, tokens)`
- `find_blocked_tokens(self, past_tokens)`

### `BadWordsProcessorV2`

**Inherits from**: LogitsProcessor

Enhanced bad words filtering processor.

Filters out tokens that would complete a "bad word" sequence.
Supports n-gram matching and speculative decoding.

**Methods** (12):
- `__init__(self, max_num_reqs, device, penalty_mode, soft_penalty)`
- `is_argmax_invariant(self)`
- `update_state(self, batch_update)`
- `_remove_request(self, index)`
- `_build_trie(self, bad_words)`
- `apply(self, logits)`
- `_apply_rust(self, logits)`
- `_apply_numpy(self, logits)`
- `_apply_generic(self, logits)`
- `accept_token(self, req_index, token_id)`
- ... and 2 more methods

### `BadPhrasesProcessor`

**Inherits from**: BadWordsProcessorV2

Extended processor for bad phrases with wildcards.

Beyond vLLM: Supports wildcard patterns and phrase variations.

**Methods** (3):
- `__init__(self, max_num_reqs, device, penalty_mode, max_wildcards)`
- `add_wildcard_pattern(self, req_index, prefix, suffix)`
- `_check_wildcard_match(self, past_tokens, pattern, wildcard_pos)`

## Functions (3)

### `apply_bad_words(logits, bad_words_token_ids, past_tokens_ids)`

Apply bad words filtering to logits.

Standalone function for compatibility with vLLM interface.

### `_apply_bad_words_single_batch(logits, bad_words_token_ids, past_tokens_ids)`

Apply bad words filtering for a single batch element.

### `apply_bad_words_with_drafts(logits, bad_words_token_ids, past_tokens_ids, num_draft_tokens)`

Apply bad words filtering with speculative decoding drafts.

Handles multiple draft tokens per request where logits
are flattened across draft positions.

## Dependencies

**Imports** (19):
- `LogitsProcessorV2.BatchUpdate`
- `LogitsProcessorV2.LogitsProcessor`
- `LogitsProcessorV2.MoveDirectionality`
- `LogitsProcessorV2.SamplingParams`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `rust_core`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 4 more

---
*Auto-generated documentation*
