# Class Breakdown: registry

**File**: `src\infrastructure\adapters\lora\registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRAModelEntry`

**Line**: 14  
**Methods**: 1

Entry in the LoRA registry.

[TIP] **Suggested split**: Move to `loramodelentry.py`

---

### 2. `LoRARegistry`

**Line**: 28  
**Methods**: 7

Registry for managing multiple LoRA adapters.

[TIP] **Suggested split**: Move to `loraregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
