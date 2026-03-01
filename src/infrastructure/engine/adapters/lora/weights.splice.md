# Class Breakdown: weights

**File**: `src\infrastructure\engine\adapters\lora\weights.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoRALayerWeights`

**Line**: 39  
**Methods**: 6

LoRA weights for a single layer.

[TIP] **Suggested split**: Move to `loralayerweights.py`

---

### 2. `IA3LayerWeights`

**Line**: 135  
**Methods**: 2

IA3 (Input-Activation-Attention Scaling) weights for a single layer.

[TIP] **Suggested split**: Move to `ia3layerweights.py`

---

### 3. `PackedLoRAWeights`

**Line**: 161  
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
