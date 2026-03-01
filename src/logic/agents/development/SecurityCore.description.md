# SecurityCore

**File**: `src\logic\agents\development\SecurityCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 89  
**Complexity**: 1 (simple)

## Overview

SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.

## Classes (1)

### `SecurityCore`

**Inherits from**: SecurityScannerMixin, SecurityAuditorMixin, SecurityReporterMixin

Pure logic core for security and safety validation.

**Methods** (1):
- `__init__(self, workspace_root)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `importlib.util`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.core.base.types.SecurityIssueType.SecurityIssueType`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `src.logic.agents.development.mixins.SecurityAuditorMixin.SecurityAuditorMixin`
- `src.logic.agents.development.mixins.SecurityReporterMixin.SecurityReporterMixin`
- `src.logic.agents.development.mixins.SecurityScannerMixin.SecurityScannerMixin`

---
*Auto-generated documentation*
