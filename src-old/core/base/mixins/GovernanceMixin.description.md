# GovernanceMixin

**File**: `src\core\base\mixins\GovernanceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 63  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for GovernanceMixin.

## Classes (1)

### `GovernanceMixin`

Handles resource quotas, preemption, and security clearance.

**Methods** (3):
- `__init__(self, config)`
- `suspend(self)`
- `resume(self)`

## Dependencies

**Imports** (6):
- `asyncio`
- `logging`
- `src.core.base.managers.ResourceQuotaManager.QuotaConfig`
- `src.core.base.managers.ResourceQuotaManager.ResourceQuotaManager`
- `src.logic.agents.security.FirewallAgent.FirewallAgent`
- `typing.Any`

---
*Auto-generated documentation*
