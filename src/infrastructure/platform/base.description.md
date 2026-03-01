# base

**File**: `src\infrastructure\platform\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 85  
**Complexity**: 11 (moderate)

## Overview

Base platform abstraction.

## Classes (1)

### `Platform`

**Inherits from**: ABC

Abstract base class for platform implementations.

**Methods** (11):
- `__new__(cls)`
- `get_platform_type(cls)`
- `is_available(cls)`
- `get_device_count(self)`
- `get_device_name(self, device_id)`
- `get_device_capability(self, device_id)`
- `get_memory_info(self, device_id)`
- `get_device_info(self, device_id)`
- `select_attention_backend(self, capability)`
- `is_quantization_supported(self, quant_type)`
- ... and 1 more methods

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `models.AttentionBackend`
- `models.DeviceCapability`
- `models.DeviceFeature`
- `models.DeviceInfo`
- `models.MemoryInfo`
- `models.PlatformType`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
