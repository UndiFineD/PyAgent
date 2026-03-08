#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/CoderCore.description.md

# CoderCore

**File**: `src\logic\agents\development\CoderCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 155  
**Complexity**: 3 (simple)

## Overview

Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.

## Classes (1)

### `CoderCore`

**Inherits from**: LogicCore, CoderMetricsMixin, CoderStyleMixin, CoderSmellMixin, CoderDuplicationMixin, CoderQualityMixin, CoderDocMixin, CoderValidationMixin

Core logic for CoderAgent, target for Rust conversion.

**Methods** (3):
- `__init__(self, language, workspace_root)`
- `calculate_metrics(self, content)`
- `_calculate_cyclomatic_complexity(self, node)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `ast`
- `rust_core`
- `src.core.base.AgentCore.LogicCore`
- `src.core.base.Version.VERSION`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.StyleRule.StyleRule`
- `src.core.base.types.StyleRuleSeverity.StyleRuleSeverity`
- `src.core.rust_bridge.RustBridge`
- `src.logic.agents.development.mixins.CoderDocMixin.CoderDocMixin`
- `src.logic.agents.development.mixins.CoderDuplicationMixin.CoderDuplicationMixin`
- `src.logic.agents.development.mixins.CoderMetricsMixin.CoderMetricsMixin`
- `src.logic.agents.development.mixins.CoderQualityMixin.CoderQualityMixin`
- `src.logic.agents.development.mixins.CoderSmellMixin.CoderSmellMixin`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/CoderCore.improvements.md

# Improvements for CoderCore

**File**: `src\logic\agents\development\CoderCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 155 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoderCore_test.py` with pytest tests

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


"""
Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.
"""

from src.core.base.Version import VERSION
from src.core.base.types.CodeLanguage import CodeLanguage
from src.core.base.types.CodeMetrics import CodeMetrics
from src.core.base.types.StyleRule import StyleRule
from src.core.base.types.StyleRuleSeverity import StyleRuleSeverity
from src.core.base.AgentCore import LogicCore
from src.logic.agents.development.mixins.CoderMetricsMixin import CoderMetricsMixin
from src.logic.agents.development.mixins.CoderStyleMixin import CoderStyleMixin
from src.logic.agents.development.mixins.CoderSmellMixin import CoderSmellMixin
from src.logic.agents.development.mixins.CoderDuplicationMixin import (
    CoderDuplicationMixin,
)
from src.logic.agents.development.mixins.CoderQualityMixin import CoderQualityMixin
from src.logic.agents.development.mixins.CoderDocMixin import CoderDocMixin
from src.logic.agents.development.mixins.CoderValidationMixin import (
    CoderValidationMixin,
)
import ast

__version__ = VERSION

# Logic extracted for future Rust migration (PyO3)
# Goal: Isolate all "Computationally Expensive" or "Rule-Based" logic here.

# Default style rules for Python (Re-declared here for Core access)
DEFAULT_PYTHON_STYLE_RULES: list[StyleRule] = [
    StyleRule(
        name="line_length",
        pattern=r"^.{89,}$",
        message="Line exceeds 88 characters",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="trailing_whitespace",
        pattern=r"[ \t]+$",
        message="Trailing whitespace detected",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="multiple_blank_lines",
        pattern=r"\n{4,}",
        message="More than 2 consecutive blank lines",
        severity=StyleRuleSeverity.INFO,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="missing_docstring",
        pattern=r'^def\s+\w+\([^)]*\):\s*\n\s+(?!"")',
        message="Function missing docstring",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
]


class CoderCore(
    LogicCore,
    CoderMetricsMixin,
    CoderStyleMixin,
    CoderSmellMixin,
    CoderDuplicationMixin,
    CoderQualityMixin,
    CoderDocMixin,
    CoderValidationMixin,
):
    """Core logic for CoderAgent, target for Rust conversion."""

    def __init__(
        self, language: CodeLanguage, workspace_root: str | None = None
    ) -> None:
        LogicCore.__init__(self)  # Ensure proper base init
        self.language = language
        self.workspace_root = workspace_root
        try:
            import rust_core

            self._rust_core = rust_core.CoderCore(str(language))  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            self._rust_core = None

    def calculate_metrics(self, content: str) -> CodeMetrics:
        """Analyze code structure and compute metrics."""
        from src.core.rust_bridge import RustBridge

        raw_metrics = RustBridge.calculate_metrics(content)
        if raw_metrics:
            metrics = CodeMetrics()
            metrics.lines_of_code = int(raw_metrics.get("lines_of_code", 0.0))
            metrics.lines_of_comments = int(raw_metrics.get("lines_of_comments", 0.0))
            metrics.blank_lines = int(raw_metrics.get("blank_lines", 0.0))
            metrics.cyclomatic_complexity = int(
                raw_metrics.get("cyclomatic_complexity", 1.0)
            )
            metrics.function_count = int(raw_metrics.get("function_count", 0.0))
            metrics.class_count = int(raw_metrics.get("class_count", 0.0))
            metrics.import_count = int(raw_metrics.get("import_count", 0.0))
            metrics.maintainability_index = raw_metrics.get(
                "maintainability_index", 100.0
            )
            return metrics

        lines = content.split("\n")
        metrics = CodeMetrics()

        # Basic line counts
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith("#") or stripped.startswith("//"):
                metrics.lines_of_comments += 1
            else:
                metrics.lines_of_code += 1

        # Language-specific deep analysis
        if self.language == CodeLanguage.PYTHON:
            try:
                tree = ast.parse(content)
                metrics = self._analyze_python_ast(tree, metrics)
            except SyntaxError:
                pass

        # General Maintainability Index
        metrics.maintainability_index = self.compute_maintainability_index(metrics)

        return metrics

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a function node."""
        cc = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                cc += 1
            elif isinstance(child, ast.BoolOp):
                cc += len(child.values) - 1
        return cc
