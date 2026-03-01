# ComplianceAgent

**File**: `src\classes\specialized\ComplianceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 123  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for ComplianceAgent.

## Classes (1)

### `ComplianceAgent`

**Inherits from**: BaseAgent

Phase 57: Data Privacy & Compliance.
Scans memory shards for PII and sensitive data patterns.

**Methods** (7):
- `__init__(self, path)`
- `_record(self, action, findings)`
- `scan_shard(self, shard_data)`
- `mask_pii(self, shard_data)`
- `audit_zk_fusion(self, fusion_input)`
- `generate_privacy_impact_assessment(self, project_data)`
- `_get_pia_recommendations(self, risks)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `src.classes.base_agent.BaseAgent`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
