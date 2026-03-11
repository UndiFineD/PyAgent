r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/DependencyGraphAgent.description.md

# DependencyGraphAgent

**File**: `src\classes\specialized\DependencyGraphAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for DependencyGraphAgent.

## Classes (1)

### `DependencyGraphAgent`

Maps and analyzes dependencies between agent modules and classes.
Helps in understanding the impact of changes and optimizing imports.

**Methods** (5):
- `__init__(self, workspace_path)`
- `scan_dependencies(self, start_dir)`
- `_extract_imports(self, file_path)`
- `get_impact_scope(self, module_name)`
- `generate_graph_stats(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `ast`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`
- `typing.Union`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/DependencyGraphAgent.improvements.md

# Improvements for DependencyGraphAgent

**File**: `src\classes\specialized\DependencyGraphAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 90 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DependencyGraphAgent_test.py` with pytest tests

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

import ast
import os
from pathlib import Path
from typing import Any

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

__version__ = VERSION


class DependencyGraphAgent:
    """Maps and analyzes dependencies between agent modules and classes.
    Helps in understanding the impact of changes and optimizing imports.
    """

    def __init__(self, workspace_path: str | Path) -> None:
        self.workspace_path = Path(workspace_path)
        self.dependency_map: dict[str, list[str]] = {}  # module -> list of imports

    def scan_dependencies(self, start_dir: str = "src") -> dict[str, Any]:
        """Scans a directory for Python files and extracts their imports.
        """
        search_path = self.workspace_path / start_dir
        if not search_path.exists():
            return {"error": f"Path {search_path} does not exist"}

        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    try:
                        rel_path = full_path.relative_to(self.workspace_path)
                        self.dependency_map[str(rel_path)] = self._extract_imports(
                            full_path
                        )
                    except ValueError:
                        continue

        return {"modules_scanned": len(self.dependency_map)}

    def _extract_imports(self, file_path: Path) -> list[str]:
        imports: set[str] = set()
        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except Exception:
            pass
        return list(imports)

    def get_impact_scope(self, module_name: str) -> list[str]:
        """Identifies which modules depend on a given module.
        """
        dependents = []
        for mod, imps in self.dependency_map.items():
            for imp in imps:
                # Basic check for module name in import string
                if module_name in imp or imp.startswith(module_name + "."):
                    dependents.append(mod)
                    break
        return dependents

    def generate_graph_stats(self) -> dict[str, Any]:
        """Returns complexity metrics for the dependency graph."""
        total_links = sum(len(imps) for imps in self.dependency_map.values())
        return {
            "node_count": len(self.dependency_map),
            "edge_count": total_links,
            "density": (
                total_links / (len(self.dependency_map) ** 2)
                if len(self.dependency_map) > 0
                else 0
            ),
        }
