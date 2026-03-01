# proposers

**File**: `src\infrastructure\inference\decoder\proposers.py`  
**Type**: Python Module  
**Summary**: 4 classes, 1 functions, 5 imports  
**Lines**: 331  
**Complexity**: 18 (moderate)

## Overview

Python module containing implementation for proposers.

## Classes (4)

### `DraftProposer`

**Inherits from**: Protocol

Protocol for draft token proposers.

**Methods** (2):
- `propose(self, request_id, token_ids, max_tokens)`
- `update(self, request_id, new_token_ids)`

### `NgramProposer`

N-gram based draft proposer.

Matches patterns from the prompt to propose likely continuations.

**Methods** (6):
- `__init__(self, prompt_lookup_min, prompt_lookup_max)`
- `start_request(self, request_id, prompt_token_ids)`
- `stop_request(self, request_id)`
- `propose(self, request_id, token_ids, max_tokens)`
- `_find_ngram_match(self, tokens, pattern, max_tokens)`
- `update(self, request_id, new_token_ids)`

### `SuffixNode`

Node in a suffix tree.

**Methods** (1):
- `__init__(self)`

### `SuffixProposer`

Suffix tree based draft proposer.

Builds a suffix tree from past generations and uses frequency
counts to propose likely continuations.

**Methods** (8):
- `__init__(self, max_tree_depth, max_cached_requests, max_spec_factor, min_token_prob)`
- `start_request(self, request_id, prompt_token_ids)`
- `stop_request(self, request_id)`
- `_build_tree(self, root, tokens)`
- `_maybe_evict(self)`
- `propose(self, request_id, token_ids, max_tokens)`
- `_search_tree(self, root, pattern, max_tokens)`
- `update(self, request_id, new_token_ids)`

## Functions (1)

### `ngram_match(tokens, pattern, max_continuation)`

Find n-gram pattern match in tokens.

Returns continuation tokens after the pattern match, or None if not found.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `config.DraftProposal`
- `numpy`
- `typing.Protocol`
- `typing.Sequence`

---
*Auto-generated documentation*
