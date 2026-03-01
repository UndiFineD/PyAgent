# xpu

**File**: `src\infrastructure\platform\xpu.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 88  
**Complexity**: 12 (moderate)

## Overview

Intel XPU (GPU/Accelerator) platform implementation.

## Classes (1)

### `XpuPlatform`

**Inherits from**: Platform

Intel XPU (GPU/Accelerator) platform implementation.

**Methods** (12):
- `get_platform_type(cls)`
- `is_available(cls)`
- `get_device_count(self)`
- `get_device_capability(self, device_id)`
- `get_device_name(self, device_id)`
- `get_memory_info(self, device_id)`
- `get_device_features(self, device_id)`
- `get_supported_quantizations(self)`
- `get_attention_backends(self)`
- `get_device_info(self, device_id)`
- ... and 2 more methods

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `base.Platform`
- `intel_extension_for_pytorch`
- `models.AttentionBackend`
- `models.DeviceCapability`
- `models.DeviceFeature`
- `models.DeviceInfo`
- `models.MemoryInfo`
- `models.PlatformType`
- `models.QuantizationType`
- `torch`
- `typing.List`
- `typing.Set`
- ... and 1 more

---
*Auto-generated documentation*
