# Class Breakdown: weights

**File**: `src\infrastructure\adapters\lora\weights.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRALayerWeights`

**Line**: 15  
**Methods**: 6

LoRA weights for a single layer.

[TIP] **Suggested split**: Move to `loralayerweights.py`

---

### 2. `PackedLoRAWeights`

**Line**: 69  
**Methods**: 3

Packed LoRA weights for fused QKV or gate+up projections.

[TIP] **Suggested split**: Move to `packedloraweights.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
