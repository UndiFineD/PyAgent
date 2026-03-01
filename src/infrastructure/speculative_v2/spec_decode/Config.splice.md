# Class Breakdown: Config

**File**: `src\infrastructure\speculative_v2\spec_decode\Config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `VerificationStrategy`

**Line**: 12  
**Inherits**: Enum  
**Methods**: 0

Verification strategy for speculative decoding.

[TIP] **Suggested split**: Move to `verificationstrategy.py`

---

### 2. `AcceptancePolicy`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

Policy for accepting draft tokens.

[TIP] **Suggested split**: Move to `acceptancepolicy.py`

---

### 3. `SpecDecodeConfig`

**Line**: 29  
**Methods**: 0

Configuration for speculative decoding verification.

[TIP] **Suggested split**: Move to `specdecodeconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
