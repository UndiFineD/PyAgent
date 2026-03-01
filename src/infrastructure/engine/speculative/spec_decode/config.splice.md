# Class Breakdown: config

**File**: `src\infrastructure\engine\speculative\spec_decode\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `VerificationStrategy`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

Verification strategy regarding speculative decoding.

[TIP] **Suggested split**: Move to `verificationstrategy.py`

---

### 2. `AcceptancePolicy`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Policy regarding accepting draft tokens.

[TIP] **Suggested split**: Move to `acceptancepolicy.py`

---

### 3. `SpecDecodeConfig`

**Line**: 46  
**Methods**: 0

Configuration regarding speculative decoding verification.

[TIP] **Suggested split**: Move to `specdecodeconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
