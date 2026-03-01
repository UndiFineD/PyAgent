# tensor

**File**: `src\infrastructure\quantization\engine\tensor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 79  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for tensor.

## Classes (1)

### `QuantizedTensor`

Quantized tensor representation.

**Methods** (4):
- `__init__(self, data, scale, zero_point, shape, config)`
- `dequantize(self)`
- `memory_bytes(self)`
- `compression_ratio(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `config.QuantConfig`
- `numpy`
- `numpy.typing.NDArray`
- `typing.TYPE_CHECKING`
- `utils.unpack_int4`

---
*Auto-generated documentation*
