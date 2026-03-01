# ModelRegistry

**File**: `src\infrastructure\models\ModelRegistry.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 11 imports  
**Lines**: 51  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ModelRegistry.

## Functions (4)

### `register_model(spec)`

Register a model architecture.

### `get_model_info(name, config)`

Get information for a model.

### `detect_architecture(name, config)`

Detect architecture from name or config.

### `estimate_vram(name, ctx, quant)`

Estimate VRAM usage for a model.

## Dependencies

**Imports** (11):
- `registry.ArchitectureDetector`
- `registry.ArchitectureSpec`
- `registry.ModelArchitecture`
- `registry.ModelCapability`
- `registry.ModelConfig`
- `registry.ModelFormat`
- `registry.ModelInfo`
- `registry.ModelRegistry`
- `registry.QuantizationType`
- `registry.VRAMEstimate`
- `registry.VRAMEstimator`

---
*Auto-generated documentation*
