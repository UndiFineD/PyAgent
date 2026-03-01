# registry

**File**: `src\core\base\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 6 (moderate)

## Overview

AgentRegistry: Central registry for all active agent instances.
Provides discovery and cross-agent communication.

## Classes (1)

### `AgentRegistry`

Singleton registry to track all active agents.

**Methods** (6):
- `__new__(cls)`
- `register(self, agent)`
- `unregister(self, name)`
- `get_agent(self, name)`
- `list_agents(self)`
- `active_count(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
