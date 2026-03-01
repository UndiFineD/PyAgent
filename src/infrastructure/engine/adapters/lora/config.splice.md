# Class Breakdown: config

**File**: `src\infrastructure\engine\adapters\lora\config.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRATarget`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Common LoRA target modules.

[TIP] **Suggested split**: Move to `loratarget.py`

---

### 2. `LoRAConfig`

**Line**: 40  
**Methods**: 3

Configuration for LoRA adapter.

[TIP] **Suggested split**: Move to `loraconfig.py`

---

### 3. `LoRAModelState`

**Line**: 71  
**Inherits**: Enum  
**Methods**: 0

State of a LoRA model in the manager.

[TIP] **Suggested split**: Move to `loramodelstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
