# Splice: src/infrastructure/engine/loading/kv_offload/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- OffloadMedium
- LoadStoreSpec
- BlockStatus
- OffloadingEvent
- PrepareStoreOutput

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
