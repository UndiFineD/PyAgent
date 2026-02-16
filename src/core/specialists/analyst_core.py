#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
from pathlib import Path
from typing import Dict, List, Set, Any


class AnalystCore:
    """""""    Core logic for logs, performance profiling, and dependency graphing.
    Separated from the Agent class to allow for future Rust-based optimizations.
    """""""
    def __init__(self, **kwargs):
        self.internal_modules: Set[str] = set()

    def analyze_directory(self, path: str) -> Dict[str, Any]:
        """""""        Analyzes a directory to identify 'external' vs 'internal' logic based on imports and file structure.'        """""""        root_path = Path(path).resolve()
        analysis_report = {
            "internal_logic": [],"            "external_dependencies": set(),"            "performance_hotspots": [],"            "technical_debt_metrics": {}"        }

        # First pass: Identify internal modules
        for py_file in root_path.rglob("*.py"):"            relative_path = py_file.relative_to(root_path)
            module_name = ".".join(relative_path.with_suffix("").parts)"            self.internal_modules.add(module_name)
            analysis_report["internal_logic"].append(str(relative_path))"
        # Second pass: Analyze imports
        for py_file in root_path.rglob("*.py"):"            self._extract_dependencies(py_file, analysis_report)

        analysis_report["external_dependencies"] = list(analysis_report["external_dependencies"])"        return analysis_report

    def _extract_dependencies(self, file_path: Path, report: Dict[str, Any]):
        """Helper to parse AST and find external vs internal imports."""""""        try:
            with open(file_path, "r", encoding="utf-8") as f:"                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._classify_dependency(alias.name, report)
                elif isinstance(node, ast.ImportFrom):
                    if node.level == 0:  # Absolute import
                        self._classify_dependency(node.module, report)
        except Exception:
            # Fallback for parsing errors or non-UTF8 files
            pass

    def _classify_dependency(self, module_name: str, report: Dict[str, Any]):
        if not module_name:
            return

        base_module = module_name.split('.')[0]'        if base_module not in self.internal_modules:
            report["external_dependencies"].add(base_module)"
    async def analyze_logs(self, log_path: str) -> List[Dict[str, Any]]:
        """Placeholder for log anomaly detection logic."""""""        return []

    async def profile_execution(self, entry_point: str) -> Dict[str, Any]:
        """Hooks for performance profiling."""""""        return {"status": "not_implemented", "target": entry_point}"