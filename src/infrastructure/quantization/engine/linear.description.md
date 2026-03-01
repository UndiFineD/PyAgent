# linear

**File**: `src\infrastructure\quantization\engine\linear.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 173  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for linear.

## Classes (1)

### `LinearQuantizer`

**Inherits from**: Quantizer

Linear (uniform) quantization.

**Methods** (8):
- `quantize(self, weight)`
- `dequantize(self, qtensor)`
- `_compute_tensor_params(self, weight)`
- `_compute_channel_params(self, weight)`
- `_compute_group_params(self, weight)`
- `_quantize_linear(self, weight, scale, zp)`
- `_quantize_per_channel(self, weight, scale, zp)`
- `_quantize_per_group(self, weight, scale, zp)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `base.Quantizer`
- `config.QuantStrategy`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.TYPE_CHECKING`
- `utils.pack_int4`

---
*Auto-generated documentation*
