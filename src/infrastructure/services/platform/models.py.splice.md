# Splice: src/infrastructure/services/platform/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PlatformType
- CpuArchitecture
- QuantizationType
- AttentionBackend
- DeviceFeature
- DeviceCapability
- MemoryInfo
- DeviceInfo
- PlatformConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
