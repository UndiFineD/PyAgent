"""
LLM_CONTEXT_START

## Source: src-old/core/modules/CodeQualityModule.description.md

# CodeQualityModule

**File**: `src\core\modules\CodeQualityModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 88  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for CodeQualityModule.

## Classes (1)

### `CodeQualityModule`

**Inherits from**: BaseModule

Consolidated core module for code quality analysis.
Migrated from CodeQualityCore.

**Methods** (7):
- `initialize(self)`
- `execute(self, source, language)`
- `calculate_score(self, issues_count)`
- `check_python_source_quality(self, source)`
- `analyze_rust_source(self, source)`
- `analyze_js_source(self, source)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/modules/CodeQualityModule.improvements.md

# Improvements for CodeQualityModule

**File**: `src\core\modules\CodeQualityModule.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 88 lines (small)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CodeQualityModule_test.py` with pytest tests

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

import re
from typing import Any, Dict, List
from src.core.base.modules import BaseModule


class CodeQualityModule(BaseModule):
    """
    Consolidated core module for code quality analysis.
    Migrated from CodeQualityCore.
    """

    def initialize(self) -> bool:
        """Load quality thresholds and regex patterns."""
        return super().initialize()

    def execute(self, source: str, language: str = "python") -> list[dict[str, Any]]:
        """
        Analyzes source code quality for a specific language.
        """
        if not self.initialized:
            self.initialize()

        if language.lower() == "python":
            return self.check_python_source_quality(source)
        elif language.lower() == "rust":
            return self.analyze_rust_source(source)
        elif language.lower() in ["javascript", "js", "typescript", "ts"]:
            return self.analyze_js_source(source)
        return []

    def calculate_score(self, issues_count: int) -> int:
        """Calculates a quality score based on the number of issues."""
        return max(0, 100 - (issues_count * 5))

    def check_python_source_quality(self, source: str) -> list[dict[str, Any]]:
        """Analyzes Python source code for style issues."""
        issues = []
        lines = source.splitlines()
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(
                    {
                        "line": i,
                        "type": "Style",
                        "message": "Line too long (>120 chars)",
                    }
                )
        return issues

    def analyze_rust_source(self, source: str) -> list[dict[str, Any]]:
        """Analyzes Rust source for common patterns/issues."""
        issues = []
        if not source or len(source.strip()) < 5:
            issues.append(
                {
                    "type": "Suggestion",
                    "message": "clippy: source too sparse for deep analysis.",
                }
            )
        if "unwrap()" in source:
            issues.append(
                {
                    "type": "Safety",
                    "message": "Avoid '.unwrap()', use proper error handling or '.expect()'.",
                }
            )
        if "match" in source and source.count("=>") == 1:
            issues.append(
                {
                    "type": "Suggestion",
                    "message": "Consider using 'if let' instead of 'match' for single pattern.",
                }
            )
        return issues

    def analyze_js_source(self, source: str) -> list[dict[str, Any]]:
        """Analyzes JavaScript source for common patterns/issues."""
        issues = []
        if re.search(r"\bvar\s+", source):
            issues.append(
                {
                    "type": "Insecure",
                    "message": "Avoid using 'var', use 'let' or 'const' instead.",
                }
            )
        if "==" in source and "===" not in source:
            issues.append(
                {
                    "type": "Style",
                    "message": "Use '===' instead of '==' for strict equality check.",
                }
            )
        return issues

    def shutdown(self) -> bool:
        """Cleanup quality analyzer."""
        return super().shutdown()
