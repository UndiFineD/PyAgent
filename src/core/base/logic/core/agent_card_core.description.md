# agent_card_core

**File**: `src\core\base\logic\core\agent_card_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for agent_card_core.

## Classes (3)

### `AgentCapability`

**Inherits from**: BaseModel

Class AgentCapability implementation.

### `AgentCard`

**Inherits from**: BaseModel

Standardized manifest for cross-agent discovery.
Pattern harvested from agentic_design_patterns.

### `AgentCardCore`

Manages a registry of AgentCards for inter-agent communication (A2A).

**Methods** (5):
- `__init__(self)`
- `register_agent(self, card)`
- `find_agents_by_capability(self, capability_query)`
- `get_agent_manifest(self, agent_id)`
- `export_all_cards(self)`

## Dependencies

**Imports** (6):
- `pydantic.BaseModel`
- `pydantic.Field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
