# PrivacyScannerMixin

**File**: `src\logic\agents\security\mixins\PrivacyScannerMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 45  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for PrivacyScannerMixin.

## Classes (1)

### `PrivacyScannerMixin`

Mixin for PII scanning and masking in ComplianceAgent.

**Methods** (3):
- `scan_shard(self, shard_data)`
- `mask_pii(self, shard_data)`
- `audit_zk_fusion(self, fusion_input)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `re`
- `src.logic.agents.security.ComplianceAgent.ComplianceAgent`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
