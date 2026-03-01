# __init__

**File**: `src\infrastructure\speculative_v2\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 13 imports  
**Lines**: 71  
**Complexity**: 0 (simple)

## Overview

Speculative Decoding v2: Tree-based speculation with multiple proposers.

Provides:
- SpeculativeDecoder: Main orchestrator for speculative decoding
- NgramProposer: N-gram based token prediction
- MedusaProposer: Multi-head parallel prediction
- SpeculativeVerifier: Token acceptance verification
- SpeculativeTree: Tree structure for candidate tokens

## Dependencies

**Imports** (13):
- `SpeculativeDecoder.AcceptanceMethod`
- `SpeculativeDecoder.MedusaProposer`
- `SpeculativeDecoder.NgramProposer`
- `SpeculativeDecoder.ProposerStats`
- `SpeculativeDecoder.ProposerType`
- `SpeculativeDecoder.SpeculativeDecoder`
- `SpeculativeDecoder.SpeculativeProposer`
- `SpeculativeDecoder.SpeculativeToken`
- `SpeculativeDecoder.SpeculativeTree`
- `SpeculativeDecoder.SpeculativeVerifier`
- `SpeculativeDecoder.VerificationResult`
- `SpeculativeDecoder.create_medusa_decoder`
- `SpeculativeDecoder.create_ngram_decoder`

---
*Auto-generated documentation*
