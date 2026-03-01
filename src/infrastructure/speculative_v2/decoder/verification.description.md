# verification

**File**: `src\infrastructure\speculative_v2\decoder\verification.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 130  
**Complexity**: 6 (moderate)

## Overview

Verifies speculative tokens against target model outputs.

## Classes (2)

### `VerificationResult`

Result of speculative token verification.

**Methods** (1):
- `success(self)`

### `SpeculativeVerifier`

Verifies speculative tokens against target model.

**Methods** (5):
- `__init__(self, vocab_size, method, temperature)`
- `verify_greedy(self, proposed_tokens, target_logits)`
- `verify_speculative(self, proposed_tokens, draft_probs, target_logits)`
- `verify(self, proposed_tokens, target_logits, draft_probs)`
- `acceptance_rate(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `config.AcceptanceMethod`
- `dataclasses.dataclass`
- `numpy`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
