# Splice: src/infrastructure/engine/engine_core_client.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RequestType
- ClientConfig
- EngineCoreClient
- InprocClient
- SyncMPClient
- AsyncMPClient

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
