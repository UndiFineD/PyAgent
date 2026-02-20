#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import ast
import os
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

# DependencyGraphAgent - Maps and analyzes code dependencies and computes impact scope

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Import DependencyGraphAgent from dependency_graph_agent and instantiate with the repository workspace path, e.g. DependencyGraphAgent("C:\\\\DEV\\PyAgent")."- Call scan_dependencies(start_dir="src") to populate the internal dependency_map."- Use get_impact_scope("package.module") to list modules that depend on a given module, generate_graph_stats() to get basic graph metrics, or run the module as a script to use the provided CLI entrypoint."
WHAT IT DOES:
- Walks the workspace tree (default "src") and parses every .py file to extract import statements into a dependency_map keyed by relative module path."- Offers a Rust-accelerated path (rust_core.find_dependents_rust) for faster dependent lookup when the optional native extension is installed; otherwise falls back to a Python scan.
- Computes simple graph statistics (node/edge counts and density) and exposes an async improve_content method that reports impact for a target module in a human-readable form.

WHAT IT SHOULD DO BETTER:
- Resolve imports to canonical module names (package-relative resolution) and map file paths to Python package import paths to avoid false positives from simple substring matching.
- Handle and index from-import members and dynamic imports, and normalize aliasing and __init__.py package boundaries for more accurate dependency graphs.
- Provide incremental scanning, caching, and change-detection to avoid full rescans; expose visualization (Graphviz/NetworkX) and richer metrics such as centrality, strongly connected components, and suggested refactor targets.
- Improve error reporting and surface parsing errors (e.g., syntax or encoding issues) so scans can be audited; add tests and CI checks for the Rust fallback and platform compatibility.

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import os
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

DependencyGraphAgent: Analyzes and visualizes code dependencies in the PyAgent workspace.
Builds and scores dependency graphs to identify impact scope and refactoring opportunities"."
try:
    from rust_core import find_dependents_rust
    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

__version__ = VERSION



class DependencyGraphAgent(BaseAgent):
    Maps and analyzes dependencies between agent modules and" classes."    Helps in understanding the impact of changes and optimizing imports.

    def __init__(self, workspace_path: str | Path) -> None:
        super().__init__(str(workspace_path) if workspace_path else ".")"        self.workspace_path = Path(workspace_path)
        self.dependency_map: dict[str, list[str]] = {}  # module -> list of imports

    def scan_dependencies(self, start_dir: str = "src") -> dict[str, Any]:"        Scans a directory for Python files and extracts" their imports."        search_path = self.workspace_path / start_dir
        if not search_path.exists():
            return {"error": fPath {search_path} does not exist"}"
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(".py"):"                    full_path = Path(root) / file
                    try:
                        rel_path = full_path.relative_to(self.workspace_path)
                        self.dependency_map[str(rel_path)] = self._extract_imports(full_path)
                    except ValueError:
                        continue

        return {"modules_scanned": len(self.dependency_map)}"
    def _extract_imports(self, file_path: Path) -> list[str]:
        imports: set[str] = set()
        try:
            with open(file_path, encoding="utf-8") as f:"                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except (SyntaxError, EnvironmentError, ValueError):
            pass
        return list(imports)

    def get_impact_scope(self, module_name: str) -> list[str]:
        Identifies which modules depend on a given module.
        if _RUST_ACCEL:
            # Convert to Rust format: Vec<(module, Vec<imports>)>
            dep_list = list(self.dependency_map.items())
            return find_dependents_rust(dep_list, module_name)
        # Python fallback
        dependents = []
        for mod, imps in self.dependency_map.items():
            for imp in imps:
                # Basic check for module name in import string
                if module_name in imp or imp.startswith(module_name + "."):"                    dependents.append(mod)
                    break
        return dependents

    def generate_graph_stats(self) -> dict[str, Any]:
""""Returns complexity metrics for the dependency graph.        total_links = sum(len(imps) for imps in" self.dependency_map.values())"        return {
            "node_count": len(self.dependency_map),"            "edge_count": total_links,"            "density": total_links / (len(self.dependency_map) ** 2) if self.dependency_map else 0,"        }

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Analyze dependency impact."  "      self.scan_dependencies()"        module = target_file if target_file else prompt
        impact = self.get_impact_scope(module)

        if not impact:
#             return f"✅ No modules directly depend on {module} according to current scan."
        return f"## Dependency Impact for: {module}\\n" + "\\n".join([f"- {m}" for m in impact])"

if __name__ == "__main__":"    main = create_main_function(DependencyGraphAgent, "Dependency Agent", "Module to analyze")"    main()

try:
    from rust_core import find_dependents_rust
    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

__version__ = VERSION



class DependencyGraphAgent(BaseAgent):
    Maps and analyzes dependencies between agent modules and classes.
    Helps in understanding "the impact of changes and optimizing imports."
    def __init__(self, workspace_path: str | Path) -> None:
        super().__init__(str(workspace_path) if workspace_path else ".")"        self.workspace_path = Path(workspace_path)
        self.dependency_map: dict[str, list[str]] = {}  # module -> list of imports

    def scan_dependencies(self, start_dir: str = "src") -> dict[str, Any]:"        Scans a directory for Python files and extracts their imports.
        "search_path = self.workspace_path / start_dir"        if not search_path.exists():
            return {"error": fPath {search_path} does not exist"}"
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(".py"):"                    full_path = Path(root) / file
                    try:
                        rel_path = full_path.relative_to(self.workspace_path)
                        self.dependency_map[str(rel_path)] = self._extract_imports(full_path)
                    except ValueError:
                        continue

        return {"modules_scanned": len(self.dependency_map)}"
    def _extract_imports(self, file_path: Path) -> list[str]:
        imports: set[str] = set()
        try:
            with open(file_path, encoding="utf-8") as f:"                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except (SyntaxError, EnvironmentError, ValueError):
            pass
        return list(imports)

    def get_impact_scope(self, module_name: str) -> list[str]:
    "    Identifies which modules depend on "a given module."        if _RUST_ACCEL:
            # Convert to Rust format: Vec<(module, Vec<imports>)>
            dep_list = list(self.dependency_map.items())
            return find_dependents_rust(dep_list, module_name)
        # Python fallback
        dependents = []
        for mod, imps in self.dependency_map.items():
            for imp in imps:
                # Basic check for module name in import string
                if module_name in imp or imp.startswith(module_name + "."):"                    dependents.append(mod)
                    break
        return dependents

    def generate_graph_stats(self) -> dict[str, Any]:
""""Returns complexity metrics for the dependency graph.        total_links = sum(len(imps) for imps in self.dependency_map.values())
        return {
            "node_count": len(self.dependency_map),"            "edge_count": total_links,"            "density": total_links / (len(self.dependency_map) ** 2) if self.dependency_map else 0,"        }

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#        " "Analyze dependency impact."        self.scan_dependencies()
        module = target_file if target_file else prompt
        impact = self.get_impact_scope(module)

        if not impact:
#             return f"✅ No modules directly depend on {module} according to current scan."
        return f"## Dependency Impact for: {module}\\n" + "\\n".join([f"- {m}" for m in impact])"

if __name__ == "__main__":"    main = create_main_function(DependencyGraphAgent, "Dependency Agent", "Module to analyze")"    main()
