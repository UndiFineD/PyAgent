#!/usr/bin/env python3


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



# ImpactAnalyzer - Analyze error impact across files and functions

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # [Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
# USAGE:
Instantiate ImpactAnalyzer, populate with add_dependency(file, depends_on) and add_functions(file, functions), then call analyze(error: ErrorEntry) to receive an ErrorImpact describing affected files, functions, downstream effects and an impact_score. Example:
analyzer = ImpactAnalyzer()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # analyzer.add_dependency("a.py", ["b.py"])
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # analyzer.add_functions("a.py", ["foo", "bar"])
impact = analyzer.analyze(error_entry)

# WHAT IT DOES:
# Provides a lightweight in-memory analysis of which files and functions are affected by a reported error by scanning recorded file dependencies and function lists; computes a simple numeric impact score based on severity, number of affected files, and functions; and discovers downstream effects via a recursive traversal of the dependency graph.

# WHAT IT SHOULD DO BETTER:
# - Normalize and validate file paths and handle multiple path representations to avoid missed matches.
# - Include transitive impact weighting (distance-based decay) and configurable scoring rather than hard-coded multipliers and caps.
# - Detect and handle cyclic dependencies more explicitly; currently recursion guards prevent infinite loops but reporting could be improved.
# - Support function-level dependency resolution (call graph analysis) rather than assuming functions are only within the error's file."  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
# - Provide async APIs or batching for large repositories and integrate with AST or static analysis to discover dependencies automatically.
# - Add unit tests and benchmarks for scoring behavior and graph traversal performance; expose tuning parameters for production use.

# FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py


from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .error_entry import ErrorEntry
from .error_impact import ErrorImpact
from .error_severity import ErrorSeverity

__version__ = VERSION


class ImpactAnalyzer:
    Analyzes the impact of errors on the codebase.

    Determines which files and functions are affected by errors
    and calculates impact scores.

    Attributes:
        file_dependencies: Map of file dependencies.
    

    def __init__(self) -> None:
        Initialize the impact analyzer.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.file_dependencies: dict[str, list[str]] = {}
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.function_map: dict[str, list[str]] = {}

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def add_dependency(self, file: str, depends_on: list[str]) -> None:
        Add file dependencies.

        Args:
            file: The file path.
            depends_on: List of files this file depends on.
        
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.file_dependencies[file] = depends_on

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def add_functions(self, file: str, functions: list[str]) -> None:
        Add functions in a file.

        Args:
            file: The file path.
            functions: List of function names in the file.
        
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.function_map[file] = functions

    def analyze(self, error: ErrorEntry) -> ErrorImpact:
        Analyze the impact of an error.

        Args:
            error: The error to analyze.

        Returns:
            ErrorImpact with affected files and functions.
        
        affected_files = self._find_affected_files(error.file_path)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         affected_functions = self.function_map.get(error.file_path, [])
        downstream = self._find_downstream_effects(error.file_path)

        impact_score = self._calculate_impact_score(len(affected_files), len(affected_functions), error.severity)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         return ErrorImpact(
            error_id=error.id,
            affected_files=affected_files,
            affected_functions=affected_functions,
            downstream_effects=downstream,
            impact_score=impact_score,
        )

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_affected_files(self, file_path: str) -> list[str]:
        Find files that depend on the given file.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         affected: list[str] = []
        for file, deps in self.file_dependencies.items():
            if file_path in deps:
                affected.append(file)
        return affected

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_downstream_effects(self, file_path: str) -> list[str]:
        Find downstream effects recursively.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         effects: list[str] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         visited: set[str] = set()
        self._find_downstream_recursive(file_path, effects, visited)
        return effects

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_downstream_recursive(self, file_path: str, effects: list[str], visited: set[str]) -> None:
        Recursively find downstream effects.
        if file_path in visited:
            return
        visited.add(file_path)
        for file, deps in self.file_dependencies.items():
            if file_path in deps and file not in effects:
                effects.append(file)
                self._find_downstream_recursive(file, effects, visited)

    def _calculate_impact_score(self, file_count: int, func_count: int, severity: ErrorSeverity) -> float:
        Calculate an impact score.
        base = severity.value * 10
        file_impact = min(file_count * 5, 30)
        func_impact = min(func_count * 2, 20)
        return min(100, base + file_impact + func_impact)


from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .error_entry import ErrorEntry
from .error_impact import ErrorImpact
from .error_severity import ErrorSeverity

__version__ = VERSION


class ImpactAnalyzer:
    Analyzes the impact of errors on the codebase.

    Determines which files and functions are affected by errors
    and calculates impact scores.

    Attributes:
        file_dependencies: Map of file dependencies.
    

    def __init__(self) -> None:
        Initialize the impact analyzer.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.file_dependencies: dict[str, list[str]] = {}
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.function_map: dict[str, list[str]] = {}

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def add_dependency(self, file: str, depends_on: list[str]) -> None:
        Add file dependencies.

        Args:
            file: The file path.
            depends_on: List of files this file depends on.
        
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.file_dependencies[file] = depends_on

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def add_functions(self, file: str, functions: list[str]) -> None:
        Add functions in a file.

        Args:
            file: The file path.
            functions: List of function names in the file.
        
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.function_map[file] = functions

    def analyze(self, error: ErrorEntry) -> ErrorImpact:
        Analyze the impact of an error.

        Args:
            error: The error to analyze.

        Returns:
            ErrorImpact with affected files and functions.
        
        affected_files = self._find_affected_files(error.file_path)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         affected_functions = self.function_map.get(error.file_path, [])
        downstream = self._find_downstream_effects(error.file_path)

        impact_score = self._calculate_impact_score(len(affected_files), len(affected_functions), error.severity)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         return ErrorImpact(
            error_id=error.id,
            affected_files=affected_files,
            affected_functions=affected_functions,
            downstream_effects=downstream,
            impact_score=impact_score,
        )

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_affected_files(self, file_path: str) -> list[str]:
        Find files that depend on the given file.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         affected: list[str] = []
        for file, deps in self.file_dependencies.items():
            if file_path in deps:
                affected.append(file)
        return affected

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_downstream_effects(self, file_path: str) -> list[str]:
        Find downstream effects recursively.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         effects: list[str] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         visited: set[str] = set()
        self._find_downstream_recursive(file_path, effects, visited)
        return effects

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _find_downstream_recursive(self, file_path: str, effects: list[str], visited: set[str]) -> None:
        Recursively find downstream effects.
        if file_path in visited:
            return
        visited.add(file_path)
        for file, deps in self.file_dependencies.items():
            if file_path in deps and file not in effects:
                effects.append(file)
                self._find_downstream_recursive(file, effects, visited)

    def _calculate_impact_score(self, file_count: int, func_count: int, severity: ErrorSeverity) -> float:
        Calculate an impact score.
        base = severity.value * 10
        file_impact = min(file_count * 5, 30)
        func_impact = min(func_count * 2, 20)
        return min(100, base + file_impact + func_impact)
