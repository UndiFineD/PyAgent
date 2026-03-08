# SecurityReporterMixin

**File**: `src\logic\agents\development\mixins\SecurityReporterMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 50  
**Complexity**: 2 (simple)

## Overview

Reporting and recording logic for SecurityCore.

## Classes (1)

### `SecurityReporterMixin`

Mixin for security reporting and recording findings.

**Methods** (2):
- `_record_finding(self, issue_type, severity, desc)`
- `get_risk_level(self, vulnerabilities)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `src.core.base.types.SecurityVulnerability.SecurityVulnerability`
- `time`

---
*Auto-generated documentation*
