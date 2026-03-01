# Class Breakdown: models

**File**: `src\infrastructure\compute\backend\vllm_advanced\lora\models.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AdapterState`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

State of a LoRA adapter.

[TIP] **Suggested split**: Move to `adapterstate.py`

---

### 2. `LoraConfig`

**Line**: 51  
**Methods**: 0

Configuration for LoRA loading and management.

[TIP] **Suggested split**: Move to `loraconfig.py`

---

### 3. `LoraAdapter`

**Line**: 73  
**Methods**: 3

Represents a LoRA adapter.

[TIP] **Suggested split**: Move to `loraadapter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
