# HITLConnector

**File**: `src\classes\fleet\HITLConnector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 98  
**Complexity**: 4 (simple)

## Overview

Human-in-the-loop (HITL) connector for fleet approvals.
Supports Slack and Discord notification patterns for critical agent decisions.

## Classes (1)

### `HITLConnector`

Manages external communication with humans for high-stakes approvals.

**Methods** (4):
- `__init__(self, webhook_url, workspace_root)`
- `request_approval(self, agent_id, task, context)`
- `check_approval_status(self, approval_id)`
- `get_pending_summary(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
