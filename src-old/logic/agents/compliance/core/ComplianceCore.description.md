# ComplianceCore

**File**: `src\logic\agents\compliance\core\ComplianceCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 74  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ComplianceCore.

## Classes (2)

### `ComplianceIssue`

Class ComplianceIssue implementation.

### `ComplianceCore`

Pure logic for continuous compliance auditing and regulatory scanning.
Identifies licensing conflicts, PII leaks, and dependency risks.

**Methods** (2):
- `audit_content(self, content, file_path)`
- `aggregate_score(self, issues)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `re`
- `typing.List`

---
*Auto-generated documentation*
