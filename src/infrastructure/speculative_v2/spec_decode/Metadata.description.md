# Metadata

**File**: `src\infrastructure\speculative_v2\spec_decode\Metadata.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 162  
**Complexity**: 13 (moderate)

## Overview

Metadata structures for speculative decoding.

## Classes (3)

### `SpecDecodeMetadataV2`

Enhanced metadata for speculative decoding verification.

**Methods** (8):
- `__post_init__(self)`
- `_build_cumulative_indices(self)`
- `build_logits_indices(self)`
- `record_acceptance(self, accepted)`
- `get_acceptance_rate(self)`
- `get_verification_latency(self)`
- `make_dummy(cls, draft_token_ids)`
- `from_proposals(cls, proposals)`

### `TreeVerificationMetadata`

Metadata for tree-based verification.

**Methods** (3):
- `get_path_tokens(self, path_index)`
- `get_best_path(self)`
- `from_tree(cls, tree_tokens, tree_parents)`

### `SpecDecodeMetadataFactory`

Factory for creating speculative decode metadata.

**Methods** (2):
- `create_simple(draft_tokens, num_requests)`
- `create_tree(tree_paths)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `rust_core`
- `typing.Any`

---
*Auto-generated documentation*
