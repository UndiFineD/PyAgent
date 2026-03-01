# engine

**File**: `src\infrastructure\inference\decoder\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 13 imports  
**Lines**: 143  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (1)

### `SpeculativeDecoder`

Main speculative decoding engine.

Coordinates proposer and verifier for accelerated inference.

**Methods** (9):
- `__init__(self, config)`
- `start_request(self, request_id, prompt_token_ids)`
- `stop_request(self, request_id)`
- `propose(self, request_id, current_tokens)`
- `verify(self, proposals, target_token_ids)`
- `update(self, request_id, new_token_ids)`
- `get_metrics(self)`
- `reset_metrics(self)`
- `num_active_requests(self)`

## Functions (1)

### `create_speculative_decoder(method, num_speculative_tokens)`

Create a speculative decoder with the given configuration.

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `config.DraftProposal`
- `config.SpecDecodingMetrics`
- `config.SpecMethod`
- `config.SpeculativeConfig`
- `config.VerificationResult`
- `numpy`
- `proposers.NgramProposer`
- `proposers.SuffixProposer`
- `time`
- `typing.Any`
- `typing.Sequence`
- `verification.TreeSpeculator`

---
*Auto-generated documentation*
