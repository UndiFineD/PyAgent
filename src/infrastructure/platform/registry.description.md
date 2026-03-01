# registry

**File**: `src\infrastructure\platform\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 7 functions, 18 imports  
**Lines**: 127  
**Complexity**: 12 (moderate)

## Overview

Registry for platform implementations.

## Classes (1)

### `PlatformRegistry`

Registry for platform implementations.

**Methods** (5):
- `register(cls, platform_type, platform_cls)`
- `get_platform(cls, platform_type)`
- `detect_current(cls)`
- `get_current(cls)`
- `reset(cls)`

## Functions (7)

### `get_current_platform()`

### `detect_platform()`

### `get_device_count()`

### `get_device_capability(device_id)`

### `get_memory_info(device_id)`

### `is_quantization_supported(quant_type)`

### `select_attention_backend(preferred)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `base.Platform`
- `cpu.CpuPlatform`
- `cuda.CudaPlatform`
- `logging`
- `models.AttentionBackend`
- `models.DeviceCapability`
- `models.MemoryInfo`
- `models.PlatformType`
- `models.QuantizationType`
- `rocm.RocmPlatform`
- `threading`
- `tpu.TpuPlatform`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
