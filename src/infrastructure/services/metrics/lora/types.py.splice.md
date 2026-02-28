# Splice: src/infrastructure/services/metrics/lora/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LoRALoadState
- RequestStatus
- LoRAAdapterInfo
- LoRARequestState
- LoRAStats

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
