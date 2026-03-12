"""
LLM_CONTEXT_START

## Source: src-old/core/base/core/IdentityCore.description.md

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
## Source: src-old/core/base/core/IdentityCore.improvements.md

# Improvements for IdentityCore

**File**: `src\core\base\core\IdentityCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: AgentIdentity

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `IdentityCore_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Dict, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentIdentity:
    agent_id: str
    public_key: str
    claims: dict[str, Any]


class IdentityCore:
    """Pure logic for decentralized agent identity and payload signing.
    Handles cryptographic verification and agent-ID generation.
    """

    def generate_agent_id(self, public_key: str, metadata: dict[str, Any]) -> str:
        """Generates a stable, unique agent identifier based on public key and metadata."""
        seed = f"{public_key}_{metadata.get('type', 'generic')}_{metadata.get('birth_cycle', 0)}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]

    def sign_payload(self, payload: str, secret_key: str) -> str:
        """Signs a payload using HMAC-SHA256 (simulating Ed25519 signing for pure-python)."""
        return hmac.new(
            secret_key.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()

    def verify_signature(self, payload: str, signature: str, public_key: str) -> bool:
        """Verifies a payload signature (simulated verification)."""
        # In a real implementation, this would use asymmetrical crypto.
        # For the Core logic, we simulate it by re-signing with the 'public_key'
        # as a mock secret for consistency.
        expected = self.sign_payload(payload, public_key)
        return hmac.compare_digest(expected, signature)

    def validate_identity(self, identity: AgentIdentity) -> bool:
        """Ensures the agent identity follows fleet standards."""
        return len(identity.agent_id) == 16 and "@" not in identity.agent_id
