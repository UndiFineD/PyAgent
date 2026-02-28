# Splice: src/infrastructure/compute/lora/manager/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LoRAMethod
- AdapterStatus
- TargetModule
- LoRAConfig
- LoRARequest
- LoRAInfo
- AdapterSlot

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
