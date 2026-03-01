# application_detection_core

**File**: `src\core\base\logic\core\application_detection_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 17 imports  
**Lines**: 565  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for application_detection_core.

## Classes (4)

### `ApplicationSignature`

Signature for application detection.

**Methods** (1):
- `__post_init__(self)`

### `DetectionResult`

Result of application detection.

### `DetectionConfig`

Configuration for application detection.

### `ApplicationDetectionCore`

**Inherits from**: BaseCore

Application Detection Core implementing signature-based application identification.

Inspired by THC amap, this core provides:
- Trigger packet sending
- Response signature matching
- TCP/UDP protocol support
- SSL/TLS detection
- Harmful trigger filtering

**Methods** (7):
- `__init__(self, config)`
- `_load_default_signatures(self)`
- `add_signature(self, signature)`
- `remove_signature(self, name)`
- `_matches_signature(self, response, signature)`
- `_calculate_confidence(self, result)`
- `get_detection_summary(self, results)`

## Dependencies

**Imports** (17):
- `asyncio`
- `binascii`
- `dataclasses.dataclass`
- `dataclasses.field`
- `re`
- `socket`
- `src.core.base.common.base_core.BaseCore`
- `ssl`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- `typing.Union`
- ... and 2 more

---
*Auto-generated documentation*
