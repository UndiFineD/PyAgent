# IdentityCore

**File**: `src\core\base\core\IdentityCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 38  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for IdentityCore.

## Classes (2)

### `AgentIdentity`

Class AgentIdentity implementation.

### `IdentityCore`

Pure logic for decentralized agent identity and payload signing.
Handles cryptographic verification and agent-ID generation.

**Methods** (4):
- `generate_agent_id(self, public_key, metadata)`
- `sign_payload(self, payload, secret_key)`
- `verify_signature(self, payload, signature, public_key)`
- `validate_identity(self, identity)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `hashlib`
- `hmac`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
