# verification

**File**: `src\infrastructure\inference\decoder\verification.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 90  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for verification.

## Classes (1)

### `TreeSpeculator`

Token tree speculator for batched verification.

Supports tree-structured speculation where multiple branches
can be verified in parallel.

**Methods** (3):
- `__init__(self, num_speculative_tokens, tree_width)`
- `verify_batch(self, proposals, target_logits, target_token_ids, temperature)`
- `_verify_single(self, proposal, target_token_ids, temperature)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `config.DraftProposal`
- `config.VerificationResult`
- `numpy`

---
*Auto-generated documentation*
