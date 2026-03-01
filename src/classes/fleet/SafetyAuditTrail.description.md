# SafetyAuditTrail

**File**: `src\classes\fleet\SafetyAuditTrail.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 50  
**Complexity**: 5 (moderate)

## Overview

Persistent audit log for safety violations and adversarial attempts.

## Classes (1)

### `SafetyAuditTrail`

Logs security violations for later forensic analysis and training.

**Methods** (5):
- `__init__(self, log_path)`
- `_load_log(self)`
- `log_violation(self, agent_name, task, violations, level)`
- `_save_log(self)`
- `get_summary(self)`

## Dependencies

**Imports** (4):
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`

---
*Auto-generated documentation*
