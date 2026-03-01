# Tensorizer

**File**: `src\infrastructure\tensorizer\Tensorizer.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 10 imports  
**Lines**: 41  
**Complexity**: 2 (simple)

## Overview

Tensorizer: High-performance model serialization and loading.
(Facade for modular implementation)

## Functions (2)

### `save_tensors(path, tensors, compression, verify)`

Legacy alias for save_model.

### `load_tensors(path, parallel, verify)`

Legacy alias for load_model.

## Dependencies

**Imports** (10):
- `core.CompressionType`
- `core.StreamingTensorizerReader`
- `core.TensorDtype`
- `core.TensorMetadata`
- `core.TensorizerConfig`
- `core.TensorizerReader`
- `core.TensorizerWriter`
- `core.get_model_info`
- `core.load_model`
- `core.save_model`

---
*Auto-generated documentation*
