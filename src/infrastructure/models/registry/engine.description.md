# engine

**File**: `src\infrastructure\models\registry\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 72  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (1)

### `ModelRegistry`

Central registry for model architectures.

**Methods** (8):
- `__new__(cls)`
- `__init__(self)`
- `_register_defaults(self)`
- `register(self, spec)`
- `get_model_info(self, name, config)`
- `_load_config(self, name)`
- `_estimate_params(self, c)`
- `estimate_vram(self, name, ctx, quant)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `config.ArchitectureSpec`
- `config.ModelArchitecture`
- `config.ModelCapability`
- `config.ModelInfo`
- `config.QuantizationType`
- `config.VRAMEstimate`
- `detector.ArchitectureDetector`
- `estimator.VRAMEstimator`
- `huggingface_hub.hf_hub_download`
- `json`
- `os`
- `pathlib.Path`
- `threading`
- `typing.Any`
- ... and 4 more

---
*Auto-generated documentation*
