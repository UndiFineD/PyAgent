# tpu

**File**: `src\infrastructure\platform\tpu.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 78  
**Complexity**: 12 (moderate)

## Overview

Google TPU platform implementation.

## Classes (1)

### `TpuPlatform`

**Inherits from**: Platform

Google TPU platform implementation.

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

**Imports** (13):
- `__future__.annotations`
- `base.Platform`
- `models.AttentionBackend`
- `models.DeviceCapability`
- `models.DeviceFeature`
- `models.DeviceInfo`
- `models.MemoryInfo`
- `models.PlatformType`
- `models.QuantizationType`
- `torch_xla`
- `torch_xla.core.xla_model`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
