# Verification

**File**: `src\infrastructure\speculative_v2\spec_decode\Verification.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 15 imports  
**Lines**: 149  
**Complexity**: 14 (moderate)

## Overview

Verification logic for speculative decoding.

## Classes (4)

### `VerificationResult`

Result of speculative decoding verification.

**Methods** (2):
- `all_accepted(self)`
- `acceptance_rate(self)`

### `SpecDecodeVerifier`

Verifier for speculative decoding.

**Methods** (6):
- `__init__(self, config)`
- `verify(self, metadata, draft_logprobs, target_logprobs)`
- `_verify_rejection_sampling(self, metadata, draft_logprobs, target_logprobs)`
- `_verify_typical_acceptance(self, metadata, draft_logprobs, target_logprobs)`
- `verify_tree(self, tree_metadata, draft_logprobs, target_logprobs)`
- `get_overall_acceptance_rate(self)`

### `BatchVerifier`

Batch verification for multiple requests.

**Methods** (2):
- `__init__(self, verifier)`
- `verify_batch(self, metadata_list, draft_logprobs_list, target_logprobs_list)`

### `StreamingVerifier`

Streaming verification as tokens arrive.

**Methods** (4):
- `__init__(self, config)`
- `add_token(self, token, draft_logprob, target_logprob)`
- `get_accepted(self)`
- `reset(self)`

## Dependencies

**Imports** (15):
- `Config.SpecDecodeConfig`
- `Config.VerificationStrategy`
- `Metadata.SpecDecodeMetadataV2`
- `Metadata.TreeVerificationMetadata`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `math`
- `random`
- `rust_core`
- `threading`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
