# AuthCore

**File**: `src\core\base\core\AuthCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 35  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AuthCore.

## Classes (2)

### `AuthProof`

Class AuthProof implementation.

### `AuthCore`

Pure logic for zero-knowledge-style agent authentication.
Handles challenge-response generation without secret exposure.

**Methods** (4):
- `generate_challenge(self, agent_id)`
- `generate_proof(self, challenge, secret_key)`
- `verify_proof(self, challenge, proof, expected_secret_hash)`
- `is_proof_expired(self, proof_time, ttl)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `hashlib`
- `time`

---
*Auto-generated documentation*
