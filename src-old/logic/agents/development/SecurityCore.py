#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/SecurityCore.description.md

# SecurityCore

**File**: `src\\logic\agents\\development\\SecurityCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 89  
**Complexity**: 1 (simple)

## Overview

SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.

## Classes (1)

### `SecurityCore`

**Inherits from**: SecurityScannerMixin, SecurityAuditorMixin, SecurityReporterMixin

Pure logic core for security and safety validation.

**Methods** (1):
- `__init__(self, workspace_root)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `importlib.util`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.core.base.types.SecurityIssueType.SecurityIssueType`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `src.logic.agents.development.mixins.SecurityAuditorMixin.SecurityAuditorMixin`
- `src.logic.agents.development.mixins.SecurityReporterMixin.SecurityReporterMixin`
- `src.logic.agents.development.mixins.SecurityScannerMixin.SecurityScannerMixin`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/SecurityCore.improvements.md

# Improvements for SecurityCore

**File**: `src\\logic\agents\\development\\SecurityCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 89 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityCore_test.py` with pytest tests

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


"""
SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.
"""


import importlib.util
from pathlib import Path

from src.core.base.types.SecurityIssueType import SecurityIssueType
from src.core.base.Version import VERSION
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from src.logic.agents.development.mixins.SecurityAuditorMixin import (
    SecurityAuditorMixin,
)
from src.logic.agents.development.mixins.SecurityReporterMixin import (
    SecurityReporterMixin,
)
from src.logic.agents.development.mixins.SecurityScannerMixin import (
    SecurityScannerMixin,
)

_RUST_AVAILABLE = importlib.util.find_spec("rust_core") is not None
__version__ = VERSION


class SecurityCore(SecurityScannerMixin, SecurityAuditorMixin, SecurityReporterMixin):
    """Pure logic core for security and safety validation."""

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (
            r'(?i)(password|secret|key|token|auth|pwd)\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded secret or password detected",
            "Use environment variables or a secure vault (e.g., Azure Key Vault).",
        ),
        (
            r'(?i)(api[_-]?key|access[_-]?key)\s*[:=]\s*[\'"][A-Za-z0-9/+=]{16,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Rotate the key and move it to a secure configuration provider.",
        ),
        (
            r"os\.system\s*\([^)]*\+",
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Insecure shell command construction with string concatenation",
            "Use subprocess with shell=False and pass arguments as a list.",
        ),
        (
            r"ev" + r"al\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is highly dangerous as it can execute arbitrary code",
            "Use ast.literal_eval() for safe parsing or json.loads() for data.",
        ),
        (
            r"random\.(random|randint|choice)\s*\(",
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random generator used in a potential security context",
            "Use the 'secrets' module for cryptographically strong random numbers.",
        ),
        (
            r"open\s*\([^)]*\+",
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal via unsafe file open path construction",
            "Validate file paths using Path.resolve() and ensure they are within expected boundaries.",
        ),
    ]

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root
        self.recorder = (
            LocalContextRecorder(Path(workspace_root)) if workspace_root else None
        )
