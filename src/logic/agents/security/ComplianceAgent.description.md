# ComplianceAgent

**File**: `src\logic\agents\security\ComplianceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 46  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ComplianceAgent.

## Classes (1)

### `ComplianceAgent`

**Inherits from**: BaseAgent, PrivacyScannerMixin, PrivacyAssessmentMixin

Phase 57: Data Privacy & Compliance.
Scans memory shards for PII and sensitive data patterns.

**Methods** (1):
- `__init__(self, path)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `mixins.PrivacyAssessmentMixin.PrivacyAssessmentMixin`
- `mixins.PrivacyScannerMixin.PrivacyScannerMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`

---
*Auto-generated documentation*
