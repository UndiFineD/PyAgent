# AgentStore

**File**: `src\classes\fleet\AgentStore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Agent Store for sharing specialized agent configurations and templates.
Allows agents to 'buy' or download new capabilities.

## Classes (1)

### `AgentStore`

Marketplace for agent templates and specialized configurations.

**Methods** (3):
- `__init__(self, store_path)`
- `list_templates(self)`
- `purchase_template(self, agent_id, template_name, economy)`

## Dependencies

**Imports** (8):
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
