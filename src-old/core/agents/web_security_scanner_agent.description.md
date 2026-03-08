# web_security_scanner_agent

**File**: `src\core\agents\web_security_scanner_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 141  
**Complexity**: 1 (simple)

## Overview

Module: web_security_scanner_agent
Agent for web application security scanning, refactored from aem-eye patterns.
Implements multi-agent coordination for distributed scanning tasks.

## Classes (1)

### `WebSecurityScannerAgent`

**Inherits from**: BaseAgent, SecurityMixin, DataProcessingMixin, TaskQueueMixin

Agent for web security scanning using patterns from aem-eye.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.logic.security.web_security_scanner_core.WebSecurityScannerCore`
- `src.core.base.mixins.data_processing_mixin.DataProcessingMixin`
- `src.core.base.mixins.security_mixin.SecurityMixin`
- `src.core.base.mixins.task_queue_mixin.TaskQueueMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid.UUID`

---
*Auto-generated documentation*
