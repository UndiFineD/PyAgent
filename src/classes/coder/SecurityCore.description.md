# SecurityCore

**File**: `src\classes\coder\SecurityCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 159  
**Complexity**: 7 (moderate)

## Overview

SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.

## Classes (1)

### `SecurityCore`

Pure logic core for security and safety validation.

**Methods** (7):
- `__init__(self, workspace_root)`
- `_record_finding(self, issue_type, severity, desc)`
- `scan_content(self, content)`
- `audit_command(self, command)`
- `validate_shell_script(self, script_content)`
- `scan_for_injection(self, content)`
- `get_risk_level(self, vulnerabilities)`

## Dependencies

**Imports** (12):
- `SecurityIssueType.SecurityIssueType`
- `SecurityVulnerability.SecurityVulnerability`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
