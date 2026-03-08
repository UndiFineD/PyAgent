# BaseAgent

**File**: `src\core\base\BaseAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 26 imports  
**Lines**: 292  
**Complexity**: 13 (moderate)

## Overview

BaseAgent main class and core agent logic.

## Classes (1)

### `BaseAgent`

**Inherits from**: IdentityMixin, PersistenceMixin, KnowledgeMixin, OrchestrationMixin, GovernanceMixin

Core AI Agent Shell (Synaptic modularization Phase 317).
Inherits domain logic from specialized Mixins to maintain low complexity.

**Methods** (13):
- `register_plugin(cls, name_or_plugin, plugin)`
- `unregister_plugin(cls, name)`
- `get_plugin(cls, name)`
- `__init__(self, file_path)`
- `_run_command(self, cmd, timeout)`
- `run(self, prompt)`
- `_notify_webhooks(self, event, data)`
- `get_model(self)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- ... and 3 more methods

## Dependencies

**Imports** (26):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `logging`
- `pathlib.Path`
- `requests`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.BaseAgentCore.BaseAgentCore`
- `src.core.base.ShellExecutor.ShellExecutor`
- `src.core.base.Version.VERSION`
- `src.core.base.mixins.GovernanceMixin.GovernanceMixin`
- `src.core.base.mixins.IdentityMixin.IdentityMixin`
- `src.core.base.mixins.KnowledgeMixin.KnowledgeMixin`
- `src.core.base.mixins.OrchestrationMixin.OrchestrationMixin`
- `src.core.base.mixins.PersistenceMixin.PersistenceMixin`
- ... and 11 more

---
*Auto-generated documentation*
