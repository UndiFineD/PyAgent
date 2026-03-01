# base

**File**: `src\infrastructure\quantization\engine\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 29  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for base.

## Classes (1)

### `Quantizer`

**Inherits from**: ABC

Base class for quantization algorithms.

**Methods** (3):
- `__init__(self, config)`
- `quantize(self, weight)`
- `dequantize(self, qtensor)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `config.QuantConfig`
- `numpy`
- `numpy.typing.NDArray`
- `tensor.QuantizedTensor`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
