# SecurityScanner

**File**: `src\classes\coder\SecurityScanner.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 115  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `SecurityScanner`

Scans code for security vulnerabilities.

Identifies common security issues and provides remediation guidance.

Attributes:
    vulnerabilities: List of detected vulnerabilities.

Example:
    >>> scanner=SecurityScanner()
    >>> vulns=scanner.scan("password='secret123'")

**Methods** (3):
- `__init__(self)`
- `scan(self, content)`
- `get_critical_count(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.types.SecurityIssueType.SecurityIssueType`
- `src.core.base.types.SecurityVulnerability.SecurityVulnerability`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
