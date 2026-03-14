#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/SecurityScannerMixin.description.md

# SecurityScannerMixin

**File**: `src\\logic\agents\\development\\mixins\\SecurityScannerMixin.py`  
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
## Source: src-old/logic/agents/development/mixins/SecurityScannerMixin.improvements.md

# Improvements for SecurityScannerMixin

**File**: `src\\logic\agents\\development\\mixins\\SecurityScannerMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 111 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityScannerMixin_test.py` with pytest tests

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

r"""Content scanning logic for SecurityCore."""
