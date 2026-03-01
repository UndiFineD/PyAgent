# Class Breakdown: Config

**File**: `src\infrastructure\speculative_v2\eagle\Config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EagleMethod`

**Line**: 12  
**Inherits**: Enum  
**Methods**: 0

EAGLE method variants.

[TIP] **Suggested split**: Move to `eaglemethod.py`

---

### 2. `AttentionBackend`

**Line**: 20  
**Inherits**: Enum  
**Methods**: 0

Attention backend types.

[TIP] **Suggested split**: Move to `attentionbackend.py`

---

### 3. `EagleConfig`

**Line**: 29  
**Methods**: 0

Configuration for EAGLE proposer.

[TIP] **Suggested split**: Move to `eagleconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
