# SecurityScannerMixin

**File**: `src\logic\agents\development\mixins\SecurityScannerMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 111  
**Complexity**: 3 (simple)

## Overview

Content scanning logic for SecurityCore.

## Classes (1)

### `SecurityScannerMixin`

Mixin for content and injection scanning.

**Methods** (3):
- `scan_content(self, content)`
- `scan_for_injection(self, content)`
- `_add_injection_findings(self, vulnerabilities, content)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `re`
- `rust_core.scan_lines_multi_pattern_rust`
- `src.core.base.types.SecurityIssueType.SecurityIssueType`
- `src.core.base.types.SecurityVulnerability.SecurityVulnerability`

---
*Auto-generated documentation*
