# DataPrivacyGuardAgent

**File**: `src\classes\specialized\DataPrivacyGuardAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 89  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for DataPrivacyGuardAgent.

## Classes (1)

### `PrivacyGuardAgent`

**Inherits from**: BaseAgent

Privacy Guard Agent: Monitors fleet communications for PII (Personally 
Identifiable Information), performs redaction, and tracks compliance.

**Methods** (4):
- `__init__(self, workspace_path)`
- `scan_and_redact(self, text)`
- `verify_message_safety(self, message)`
- `get_privacy_metrics(self)`

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
