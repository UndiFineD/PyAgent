# Class Breakdown: models

**File**: `src\infrastructure\services\platform\models.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PlatformType`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

Supported platform types.

[TIP] **Suggested split**: Move to `platformtype.py`

---

### 2. `CpuArchitecture`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

CPU architecture types.

[TIP] **Suggested split**: Move to `cpuarchitecture.py`

---

### 3. `QuantizationType`

**Line**: 51  
**Inherits**: Enum  
**Methods**: 0

Quantization methods.

[TIP] **Suggested split**: Move to `quantizationtype.py`

---

### 4. `AttentionBackend`

**Line**: 71  
**Inherits**: Enum  
**Methods**: 0

Attention implementation backends.

[TIP] **Suggested split**: Move to `attentionbackend.py`

---

### 5. `DeviceFeature`

**Line**: 88  
**Inherits**: Flag  
**Methods**: 0

Device feature flags.

[TIP] **Suggested split**: Move to `devicefeature.py`

---

### 6. `DeviceCapability`

**Line**: 110  
**Inherits**: NamedTuple  
**Methods**: 4

Device compute capability.

[TIP] **Suggested split**: Move to `devicecapability.py`

---

### 7. `MemoryInfo`

**Line**: 132  
**Methods**: 4

Device memory information.

[TIP] **Suggested split**: Move to `memoryinfo.py`

---

### 8. `DeviceInfo`

**Line**: 161  
**Methods**: 2

Complete device information.

[TIP] **Suggested split**: Move to `deviceinfo.py`

---

### 9. `PlatformConfig`

**Line**: 187  
**Methods**: 0

Platform configuration.

[TIP] **Suggested split**: Move to `platformconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
