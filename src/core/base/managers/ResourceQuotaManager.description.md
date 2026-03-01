# ResourceQuotaManager

**File**: `src\core\base\managers\ResourceQuotaManager.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 88  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for ResourceQuotaManager.

## Classes (3)

### `QuotaConfig`

Configuration for agent resource quotas.

### `ResourceUsage`

Current resource usage for an agent session.

**Methods** (2):
- `total_tokens(self)`
- `elapsed_time(self)`

### `ResourceQuotaManager`

Manages resource quotas and budget enforcement for agent sessions.

Phase 245: RESOURCE QUOTAS & BUDGETS

**Methods** (6):
- `__init__(self, config)`
- `update_usage(self, tokens_input, tokens_output, cycles)`
- `check_quotas(self)`
- `is_interrupted(self)`
- `interrupt_reason(self)`
- `get_report(self)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
