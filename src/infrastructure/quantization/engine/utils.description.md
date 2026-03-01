# utils

**File**: `src\infrastructure\quantization\engine\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 5 functions, 11 imports  
**Lines**: 103  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for utils.

## Functions (5)

### `pack_int4(data)`

### `unpack_int4(packed)`

### `compute_scales_minmax(weight, bits, symmetric)`

### `quantize_tensor(tensor, bits, group_size, symmetric, scheme)`

### `get_quantization_error(original, qtensor)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `awq.AWQQuantizer`
- `config.QuantConfig`
- `config.QuantScheme`
- `config.QuantStrategy`
- `gptq.GPTQQuantizer`
- `linear.LinearQuantizer`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
