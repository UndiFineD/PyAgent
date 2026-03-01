# engine

**File**: `src\infrastructure\speculative_v2\decoder\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 15 imports  
**Lines**: 117  
**Complexity**: 6 (moderate)

## Overview

Speculative decoding orchestrator.

## Classes (1)

### `SpeculativeDecoder`

Main speculative decoding orchestrator.

**Methods** (4):
- `__init__(self, vocab_size, proposer, verifier, max_speculation_depth)`
- `step(self, input_ids, target_forward_fn, num_candidates)`
- `reset(self)`
- `get_stats(self)`

## Functions (2)

### `create_ngram_decoder(vocab_size, max_depth, ngram_order)`

Create a speculative decoder with N-gram proposer.

### `create_medusa_decoder(vocab_size, num_heads, max_depth)`

Create a speculative decoder with Medusa proposer.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `config.AcceptanceMethod`
- `numpy`
- `proposers.MedusaProposer`
- `proposers.NgramProposer`
- `proposers.SpeculativeProposer`
- `tree.SpeculativeTree`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `verification.SpeculativeVerifier`
- `verification.VerificationResult`

---
*Auto-generated documentation*
