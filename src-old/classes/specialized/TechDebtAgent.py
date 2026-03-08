"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/TechDebtAgent.description.md

# TechDebtAgent

**File**: `src\classes\specialized\TechDebtAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 95  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TechDebtAgent.

## Classes (1)

### `TechDebtAgent`

**Inherits from**: BaseAgent

Analyzes the codebase for technical debt including high cyclomatic complexity,
missing docstrings, and large files.

**Methods** (3):
- `__init__(self, workspace_path)`
- `analyze_file(self, file_path)`
- `analyze_workspace(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/TechDebtAgent.improvements.md

# Improvements for TechDebtAgent

**File**: `src\classes\specialized\TechDebtAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 95 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TechDebtAgent_test.py` with pytest tests

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


from src.core.base.version import VERSION
import os
import ast
from typing import Dict, Any
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION


class TechDebtAgent(BaseAgent):
    """
    Analyzes the codebase for technical debt including high cyclomatic complexity,
    missing docstrings, and large files.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Analyzes a single Python file for technical debt."""
        if not file_path.endswith(".py"):
            return {"file": file_path, "issues": []}

        issues = []
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Check for missing docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if not ast.get_docstring(node):
                        issues.append(
                            {
                                "type": "Missing Docstring",
                                "name": getattr(node, "name", "Module"),
                                "severity": "Low",
                            }
                        )

            # Check for high complexity (simple heuristic: depth of nesting/number of nodes)
            node_count = sum(1 for _ in ast.walk(tree))
            if node_count > 1000:
                issues.append(
                    {
                        "type": "High Complexity",
                        "detail": f"File contains {node_count} AST nodes.",
                        "severity": "Medium",
                    }
                )

        except Exception as e:
            issues.append({"type": "Error", "detail": str(e), "severity": "Medium"})

        return {"file": file_path, "issues": issues, "issue_count": len(issues)}

    def analyze_workspace(self) -> dict[str, Any]:
        """Runs technical debt analysis on the entire workspace."""
        total_issues = 0
        file_reports = []

        for root, dirs, files in os.walk(self.workspace_path):
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["node_modules", "__pycache__", ".venv", "venv"]
            ]
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    report = self.analyze_file(path)
                    if report["issue_count"] > 0:
                        file_reports.append(report)
                        total_issues += report["issue_count"]

        return {
            "total_issues": total_issues,
            "hotspots": sorted(
                file_reports, key=lambda x: x["issue_count"], reverse=True
            )[:5],
        }
