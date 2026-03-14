#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/SecurityScanner.description.md

# SecurityScanner

**File**: `src\classes\coder\SecurityScanner.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 115  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `SecurityScanner`

Scans code for security vulnerabilities.

Identifies common security issues and provides remediation guidance.

Attributes:
    vulnerabilities: List of detected vulnerabilities.

Example:
    >>> scanner=SecurityScanner()
    >>> vulns=scanner.scan("password='secret123'")

**Methods** (3):
- `__init__(self)`
- `scan(self, content)`
- `get_critical_count(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.types.SecurityIssueType.SecurityIssueType`
- `src.core.base.types.SecurityVulnerability.SecurityVulnerability`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/SecurityScanner.improvements.md

# Improvements for SecurityScanner

**File**: `src\classes\coder\SecurityScanner.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 115 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityScanner_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""


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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

r"""Auto-extracted class from agent_coder.py"""
