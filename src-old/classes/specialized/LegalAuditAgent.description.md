# LegalAuditAgent

**File**: `src\classes\specialized\LegalAuditAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 94  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for LegalAuditAgent.

## Classes (1)

### `LegalAuditAgent`

**Inherits from**: BaseAgent

Phase 59: Autonomous Legal & Smart Contract Auditing.
Scans codebases for licensing risks, liability concerns, and smart contract vulnerabilities.

**Methods** (5):
- `__init__(self, path)`
- `check_license_compliance(self, content, project_license)`
- `scan_licensing(self, content)`
- `verify_smart_contract(self, logic)`
- `generate_liability_report(self, task_output)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
