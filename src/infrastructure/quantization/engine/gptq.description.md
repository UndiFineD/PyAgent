# gptq

**File**: `src\infrastructure\quantization\engine\gptq.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 107  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for gptq.

## Classes (1)

### `GPTQQuantizer`

**Inherits from**: Quantizer

GPTQ Quantization using Hessian-based optimal rounding.

**Methods** (4):
- `__init__(self, config, damp_percent, block_size)`
- `quantize(self, weight, hessian)`
- `dequantize(self, qtensor)`
- `_gptq_quantize(self, weight, hessian_inv)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `base.Quantizer`
- `config.QuantConfig`
- `linear.LinearQuantizer`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.TYPE_CHECKING`
- `utils.pack_int4`

---
*Auto-generated documentation*
