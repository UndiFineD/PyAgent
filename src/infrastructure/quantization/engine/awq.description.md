# awq

**File**: `src\infrastructure\quantization\engine\awq.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 65  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for awq.

## Classes (1)

### `AWQQuantizer`

**Inherits from**: Quantizer

Activation-Aware Weight Quantization (AWQ).

**Methods** (4):
- `__init__(self, config, calibration_data)`
- `quantize(self, weight, activations)`
- `dequantize(self, qtensor)`
- `_compute_importance(self, activations, weight)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `base.Quantizer`
- `config.QuantConfig`
- `linear.LinearQuantizer`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
