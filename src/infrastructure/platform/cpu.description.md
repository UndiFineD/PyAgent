# cpu

**File**: `src\infrastructure\platform\cpu.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 80  
**Complexity**: 10 (moderate)

## Overview

CPU-only platform implementation.

## Classes (1)

### `CpuPlatform`

**Inherits from**: Platform

CPU-only platform implementation.

**Methods** (10):
- `get_platform_type(cls)`
- `is_available(cls)`
- `get_device_count(self)`
- `get_device_capability(self, device_id)`
- `get_device_name(self, device_id)`
- `get_memory_info(self, device_id)`
- `get_device_features(self, device_id)`
- `get_supported_quantizations(self)`
- `get_attention_backends(self)`
- `select_attention_backend(self, capability)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base.Platform`
- `cpuinfo`
- `models.AttentionBackend`
- `models.CpuArchitecture`
- `models.DeviceCapability`
- `models.DeviceFeature`
- `models.MemoryInfo`
- `models.PlatformType`
- `models.QuantizationType`
- `platform`
- `psutil`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
