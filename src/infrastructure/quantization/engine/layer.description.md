# layer

**File**: `src\infrastructure\quantization\engine\layer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 49  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for layer.

## Classes (1)

### `DequantizedLinear`

Dequantized linear layer for inference.

**Methods** (5):
- `__init__(self, qweight, bias)`
- `forward(self, x, use_cache)`
- `clear_cache(self)`
- `in_features(self)`
- `out_features(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
