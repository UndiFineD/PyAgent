# Class Breakdown: config

**File**: `src\infrastructure\compute\lora\manager\config.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRAMethod`

**Line**: 27  
**Inherits**: Enum  
**Methods**: 0

LoRA method variants.

[TIP] **Suggested split**: Move to `loramethod.py`

---

### 2. `AdapterStatus`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Adapter lifecycle status.

[TIP] **Suggested split**: Move to `adapterstatus.py`

---

### 3. `TargetModule`

**Line**: 50  
**Inherits**: Enum  
**Methods**: 0

Common LoRA target modules.

[TIP] **Suggested split**: Move to `targetmodule.py`

---

### 4. `LoRAConfig`

**Line**: 65  
**Methods**: 2

LoRA adapter configuration.

[TIP] **Suggested split**: Move to `loraconfig.py`

---

### 5. `LoRARequest`

**Line**: 96  
**Methods**: 1

Request to serve with a LoRA adapter.

[TIP] **Suggested split**: Move to `lorarequest.py`

---

### 6. `LoRAInfo`

**Line**: 109  
**Methods**: 1

Information about a loaded adapter.

[TIP] **Suggested split**: Move to `lorainfo.py`

---

### 7. `AdapterSlot`

**Line**: 138  
**Methods**: 1

GPU slot for a LoRA adapter.

[TIP] **Suggested split**: Move to `adapterslot.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
