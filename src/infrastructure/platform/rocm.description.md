# rocm

**File**: `src\infrastructure\platform\rocm.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 120  
**Complexity**: 13 (moderate)

## Overview

AMD ROCm platform implementation.

## Classes (1)

### `RocmPlatform`

**Inherits from**: Platform

AMD ROCm platform implementation.

**Methods** (13):
- `get_platform_type(cls)`
- `is_available(cls)`
- `_get_torch(self)`
- `get_device_count(self)`
- `get_device_capability(self, device_id)`
- `get_device_name(self, device_id)`
- `get_memory_info(self, device_id)`
- `get_device_features(self, device_id)`
- `get_supported_quantizations(self)`
- `get_attention_backends(self)`
- ... and 3 more methods

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base.Platform`
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
