# factory

**File**: `src\infrastructure\kv_transfer\connector\factory.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 10 imports  
**Lines**: 55  
**Complexity**: 3 (simple)

## Overview

Phase 45: KV Transfer Connector Factory
Registry and factory for KV transfer connectors.

## Functions (3)

### `register_kv_connector(name, connector_cls)`

Register a KV connector class.

### `get_kv_connector(config, kv_cache_config)`

Get a KV connector instance by configuration.

### `list_kv_connectors()`

List all registered KV connectors.

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `logging`
- `src.infrastructure.kv_transfer.connector.base.KVConnectorBase`
- `src.infrastructure.kv_transfer.connector.decode_bench.DecodeBenchConnector`
- `src.infrastructure.kv_transfer.connector.types.KVTransferConfig`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
