# Splice: src/infrastructure/storage/kv_transfer/connector/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- KVConnectorRole
- KVTransferMode
- KVTransferConfig
- KVConnectorMetadata
- KVCacheBlocks
- ForwardContext
- Request

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
