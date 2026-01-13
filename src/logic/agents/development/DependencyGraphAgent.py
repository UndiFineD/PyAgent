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

from __future__ import annotations
from src.core.base.version import VERSION
import os
import ast
from pathlib import Path
from typing import Dict, List, Set, Any, Union

__version__ = VERSION

class DependencyGraphAgent:
    """
    Maps and analyzes dependencies between agent modules and classes.
    Helps in understanding the impact of changes and optimizing imports.
    """
    def __init__(self, workspace_path: str | Path) -> None:
        self.workspace_path = Path(workspace_path)
        self.dependency_map: dict[str, list[str]] = {} # module -> list of imports

    def scan_dependencies(self, start_dir: str = "src") -> dict[str, Any]:
        """
        Scans a directory for Python files and extracts their imports.
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
                        self.dependency_map[str(rel_path)] = self._extract_imports(full_path)
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
        """
        Identifies which modules depend on a given module.
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
            "density": total_links / (len(self.dependency_map) ** 2) if len(self.dependency_map) > 0 else 0
        }