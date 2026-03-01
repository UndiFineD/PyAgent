# AsyncEngineClient

**File**: `src\infrastructure\engine\AsyncEngineClient.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 14 imports  
**Lines**: 37  
**Complexity**: 0 (simple)

## Overview

AsyncEngineClient: Multi-process async engine client with DP load balancing.

Refactored to modular package structure for Phase 317.
Decomposed into types, base, and specific client implementation modules.

## Dependencies

**Imports** (14):
- `src.infrastructure.engine.engine_client.async_mp.AsyncMPClient`
- `src.infrastructure.engine.engine_client.base.EngineCoreClientBase`
- `src.infrastructure.engine.engine_client.dp_async.DPAsyncMPClient`
- `src.infrastructure.engine.engine_client.factory.auto_select_client_mode`
- `src.infrastructure.engine.engine_client.factory.create_engine_client`
- `src.infrastructure.engine.engine_client.inproc.InprocClient`
- `src.infrastructure.engine.engine_client.lb.P2CLoadBalancer`
- `src.infrastructure.engine.engine_client.sync_mp.SyncMPClient`
- `src.infrastructure.engine.engine_client.types.ClientMode`
- `src.infrastructure.engine.engine_client.types.EngineClientConfig`
- `src.infrastructure.engine.engine_client.types.EngineOutput`
- `src.infrastructure.engine.engine_client.types.SchedulerOutput`
- `src.infrastructure.engine.engine_client.types.WorkerInfo`
- `src.infrastructure.engine.engine_client.types.WorkerState`

---
*Auto-generated documentation*
