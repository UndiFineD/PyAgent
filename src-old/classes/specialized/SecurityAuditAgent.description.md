# SecurityAuditAgent

**File**: `src\classes\specialized\SecurityAuditAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 130  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for SecurityAuditAgent.

## Classes (1)

### `SecurityAuditAgent`

**Inherits from**: BaseAgent

Scans the workspace for potential security risks including hardcoded secrets,
vulnerable patterns, and insecure file permissions.

**Methods** (3):
- `__init__(self, workspace_path)`
- `scan_file(self, file_path)`
- `audit_workspace(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `os`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
