# LegalAuditAgent

**File**: `src\logic\agents\specialized\LegalAuditAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 90  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for LegalAuditAgent.

## Classes (1)

### `LegalAuditAgent`

**Inherits from**: BaseAgent

Phase 286: Legal Audit Agent.
Verifies that all source files and third-party code comply with the project's
license requirements (Apache 2.0 or MIT).

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `asyncio`
- `os`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
