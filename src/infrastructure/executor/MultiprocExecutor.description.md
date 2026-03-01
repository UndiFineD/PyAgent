# MultiprocExecutor

**File**: `src\infrastructure\executor\MultiprocExecutor.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 11 imports  
**Lines**: 31  
**Complexity**: 0 (simple)

## Overview

Phase 45: Multiprocess Executor
vLLM-inspired multiprocess executor with advanced coordination.

Refactored to modular package structure for Phase 317.
Decomposed into types, future, base, and specific implementation modules.

## Dependencies

**Imports** (11):
- `src.infrastructure.executor.multiproc.base.Executor`
- `src.infrastructure.executor.multiproc.distributed.DistributedExecutor`
- `src.infrastructure.executor.multiproc.factory.ExecutorFactory`
- `src.infrastructure.executor.multiproc.future.FutureWrapper`
- `src.infrastructure.executor.multiproc.multiproc_logic.MultiprocExecutor`
- `src.infrastructure.executor.multiproc.types.ExecutorBackend`
- `src.infrastructure.executor.multiproc.types.ResultMessage`
- `src.infrastructure.executor.multiproc.types.TaskMessage`
- `src.infrastructure.executor.multiproc.types.WorkerInfo`
- `src.infrastructure.executor.multiproc.types.WorkerState`
- `src.infrastructure.executor.multiproc.uniproc.UniprocExecutor`

---
*Auto-generated documentation*
