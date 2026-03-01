# ComplianceAgent

**File**: `src\logic\agents\compliance\ComplianceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 57  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ComplianceAgent.

## Classes (1)

### `ComplianceAgent`

**Inherits from**: BaseAgent

Shell agent for continuous compliance and regulatory auditing.
Coordinates fleet-wide scans and reports violations to the security layer.

**Methods** (2):
- `__init__(self, file_path)`
- `perform_audit(self, file_map)`

## Dependencies

**Imports** (6):
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `src.logic.agents.compliance.core.ComplianceCore.ComplianceCore`
- `typing.Any`

---
*Auto-generated documentation*
