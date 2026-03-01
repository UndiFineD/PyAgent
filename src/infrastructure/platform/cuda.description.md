# cuda

**File**: `src\infrastructure\platform\cuda.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 167  
**Complexity**: 15 (moderate)

## Overview

NVIDIA CUDA platform implementation.

## Classes (1)

### `CudaPlatform`

**Inherits from**: Platform

NVIDIA CUDA platform implementation.

**Methods** (15):
- `get_platform_type(cls)`
- `is_available(cls)`
- `_get_torch(self)`
- `get_device_count(self)`
- `get_device_capability(self, device_id)`
- `get_device_name(self, device_id)`
- `get_memory_info(self, device_id)`
- `get_device_features(self, device_id)`
- `get_driver_version(self)`
- `get_supported_quantizations(self)`
- ... and 5 more methods

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `base.Platform`
- `flash_attn`
- `logging`
- `models.AttentionBackend`
- `models.DeviceCapability`
- `models.DeviceFeature`
- `models.MemoryInfo`
- `models.PlatformType`
- `models.QuantizationType`
- `torch`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
