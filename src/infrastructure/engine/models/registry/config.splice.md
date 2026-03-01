# Class Breakdown: config

**File**: `src\infrastructure\engine\models\registry\config.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ModelCapability`

**Line**: 26  
**Inherits**: Flag  
**Methods**: 0

Model capability flags.

[TIP] **Suggested split**: Move to `modelcapability.py`

---

### 2. `ModelArchitecture`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Known model architectures.

[TIP] **Suggested split**: Move to `modelarchitecture.py`

---

### 3. `QuantizationType`

**Line**: 92  
**Inherits**: Enum  
**Methods**: 0

Quantization types.

[TIP] **Suggested split**: Move to `quantizationtype.py`

---

### 4. `ModelFormat`

**Line**: 107  
**Inherits**: Enum  
**Methods**: 0

Model file formats.

[TIP] **Suggested split**: Move to `modelformat.py`

---

### 5. `ModelConfig`

**Line**: 119  
**Methods**: 1

Model configuration.

[TIP] **Suggested split**: Move to `modelconfig.py`

---

### 6. `ArchitectureSpec`

**Line**: 138  
**Methods**: 0

Architecture specification.

[TIP] **Suggested split**: Move to `architecturespec.py`

---

### 7. `ModelInfo`

**Line**: 156  
**Methods**: 3

Information about a model.

[TIP] **Suggested split**: Move to `modelinfo.py`

---

### 8. `VRAMEstimate`

**Line**: 200  
**Methods**: 1

VRAM requirement estimation.

[TIP] **Suggested split**: Move to `vramestimate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
