#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/SecurityReporterMixin.description.md

# SecurityReporterMixin

**File**: `src\logic\agents\development\mixins\SecurityReporterMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 50  
**Complexity**: 2 (simple)

## Overview

Reporting and recording logic for SecurityCore.

## Classes (1)

### `SecurityReporterMixin`

Mixin for security reporting and recording findings.

**Methods** (2):
- `_record_finding(self, issue_type, severity, desc)`
- `get_risk_level(self, vulnerabilities)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `src.core.base.types.SecurityVulnerability.SecurityVulnerability`
- `time`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/SecurityReporterMixin.improvements.md

# Improvements for SecurityReporterMixin

**File**: `src\logic\agents\development\mixins\SecurityReporterMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityReporterMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reporting and recording logic for SecurityCore."""

import logging
import time
from src.core.base.types.SecurityVulnerability import SecurityVulnerability


class SecurityReporterMixin:
    """Mixin for security reporting and recording findings."""

    def _record_finding(self, issue_type: str, severity: str, desc: str) -> None:
        """Records security findings for fleet intelligence (Phase 108)."""
        if hasattr(self, "recorder") and self.recorder:
            try:
                self.recorder.record_lesson(
                    "security_vulnerability",
                    {
                        "type": issue_type,
                        "severity": severity,
                        "description": desc,
                        "timestamp": time.time(),
                    },
                )
            except Exception as e:
                logging.debug(f"SecurityCore: Failed to record finding: {e}")

    def get_risk_level(self, vulnerabilities: list[SecurityVulnerability]) -> str:
        """Determines the overall risk level for a report."""
        severities = [v.severity for v in vulnerabilities]
        if "critical" in severities or "CRITICAL" in [s.upper() for s in severities]:
            return "CRITICAL"
        if "high" in severities or "HIGH" in [s.upper() for s in severities]:
            return "HIGH"
        if "medium" in severities or "MEDIUM" in [s.upper() for s in severities]:
            return "MEDIUM"
        return "LOW"
