# __init__

**File**: `src\infrastructure\kv_transfer\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 9 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

KV Transfer module for disaggregated prefill-decode inference.

Provides connectors for transferring KV cache between prefill and decode instances.
Inspired by vLLM's distributed/kv_transfer/ architecture.

## Dependencies

**Imports** (9):
- `KVTransferConnector.DecodeBenchConnector`
- `KVTransferConnector.KVCacheBlocks`
- `KVTransferConnector.KVConnectorBase`
- `KVTransferConnector.KVConnectorMetadata`
- `KVTransferConnector.KVConnectorRole`
- `KVTransferConnector.KVTransferConfig`
- `KVTransferConnector.get_kv_connector`
- `KVTransferConnector.list_kv_connectors`
- `KVTransferConnector.register_kv_connector`

---
*Auto-generated documentation*
