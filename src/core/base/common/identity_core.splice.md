# Class Breakdown: identity_core

**File**: `src\core\base\common\identity_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentIdentity`

**Line**: 35  
**Methods**: 0

Immutable identity representation for a peer agent during discovery.

[TIP] **Suggested split**: Move to `agentidentity.py`

---

### 2. `IdentityCore`

**Line**: 43  
**Inherits**: BaseCore  
**Methods**: 8

Pure logic for decentralized agent identity and payload signing.
Handles cryptographic verification and agent-ID generation.

[TIP] **Suggested split**: Move to `identitycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
