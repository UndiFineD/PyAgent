# OrchestrationMixin

**File**: `src\core\base\mixins\OrchestrationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 207  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for OrchestrationMixin.

## Classes (1)

### `OrchestrationMixin`

Handles registry, tools, strategies, and distributed logging.

**Methods** (8):
- `__init__(self)`
- `strategy(self)`
- `strategy(self, value)`
- `set_strategy(self, strategy)`
- `register_tools(self, registry)`
- `log_distributed(self, level, message)`
- `get_backend_status()`
- `describe_backends()`

## Dependencies

**Imports** (18):
- `asyncio`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.BaseExceptions.CycleInterrupt`
- `src.infrastructure.backend`
- `src.infrastructure.backend.ExecutionEngine`
- `src.infrastructure.fleet.AgentRegistry.AgentRegistry`
- `src.infrastructure.orchestration.signals.SignalRegistry.SignalRegistry`
- `src.infrastructure.orchestration.system.ToolRegistry.ToolRegistry`
- `src.logic.strategies.DirectStrategy.DirectStrategy`
- `sys`
- `typing.Any`
- ... and 3 more

---
*Auto-generated documentation*
