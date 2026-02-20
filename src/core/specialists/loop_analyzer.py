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


"""
"""
Loop Analysis Utility for PyAgent Fleet

"""
This module provides reusable utilities for analyzing and detecting
anti-patterns related to for/while loops across the PyAgent codebase.
Used for performance profiling and code quality assessment.
"""
import os
import subprocess
import re
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LoopAnalysisResult:
"""
Result of loop analysis for a single file.""
file_path: str
    lines_of_code: int
    loop_count: int
    complexity_score: float
    loop_density: float  # loops per 100 lines
    has_nested_loops: bool
    has_deep_nesting: bool  # nesting > 3 levels
    has_large_loops: bool   # loops with > 50 statements


@dataclass
class LoopAnalysisConfig:
"""
Configuration for loop analysis.""
min_loc_threshold: int = 200
    min_loop_threshold: int = 3
    max_nesting_threshold: int = 3
    large_loop_threshold: int = 50
    exclude_dirs: Set[str] = None
    include_patterns: List[str] = None
    exclude_patterns: List[str] = None

    def __post_init__(self):
        if self.exclude_dirs is None:
        self.exclude_dirs = {'.venv', '__pycache__', 'node_modules', '.git'}'        if self.include_patterns is None:
        self.include_patterns = ['*.py']'        if self.exclude_patterns is None:
        self.exclude_patterns = []



class LoopAnalyzer:
"""
Reusable analyzer for detecting loop anti-patterns.""
def __init__(self, config: Optional[LoopAnalysisConfig] = None):
        self.config = config or LoopAnalysisConfig()

    def count_loops_ripgrep(self, file_path: str) -> int:
"""
Count for/while loops using ripgrep for speed.""
try:
            # Count explicit for/while statements (not in strings/comments)
            result = subprocess.run(
                ['rg', '-c', r'\\b(for|while)\\s+', file_path],'                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
            return 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # Fallback to regex if ripgrep not available
            return self._count_loops_regex(file_path)

    def _count_loops_regex(self, file_path: str) -> int:
"""
Fallback loop counting using regex.""
try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:'                content = f.read()

            # Simple regex to count for/while statements
            # This is less accurate but works without ripgrep
            loop_pattern = r'\\b(for|while)\\s+''            matches = re.findall(loop_pattern, content)

            # Filter out matches in comments and strings (basic filtering)
            filtered_matches = []
            for match in matches:
                # Basic check - if line doesn't start with # and isn't in a string'                # This is approximate but better than nothing
                filtered_matches.append(match)

            return len(filtered_matches)
        except Exception:
            return 0

    def count_lines(self, file_path: str) -> int:
"""
Count lines of code in a file.""
try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:'                return sum(1 for _ in f)
        except Exception:
            return 0

    def analyze_nesting(self, file_path: str) -> Tuple[bool, bool]:
"""
Analyze loop nesting patterns.""
try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:'                content = f.read()

            # Simple nesting analysis - count indentation levels
            lines = content.split('\\n')'            max_nesting = 0
            current_nesting = 0

            for line in lines:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):'                    continue

                # Count leading spaces/tabs (assuming 4 spaces per indent)
                indent = len(line) - len(line.lstrip())
                level = indent // 4

                if re.match(r'\\b(for|while)\\s+', stripped):'                    current_nesting = max(current_nesting, level + 1)
                    max_nesting = max(max_nesting, current_nesting)

            has_nested = max_nesting > 1
            has_deep_nesting = max_nesting > self.config.max_nesting_threshold

            return has_nested, has_deep_nesting
        except Exception:
            return False, False

    def analyze_loop_sizes(self, file_path: str) -> bool:
"""
Check for unusually large loops.""
try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:'                content = f.read()

            # Very basic loop size analysis
            # This is approximate - real analysis would need AST parsing
            lines = content.split('\\n')'            in_loop = False
            loop_start = 0

            for i, line in enumerate(lines):
                stripped = line.strip()
                if re.match(r'\\b(for|while)\\s+', stripped):'                    in_loop = True
                    loop_start = i
                elif in_loop and stripped and not stripped.startswith(' ') and not stripped.startswith('\\t'):'                    # End of loop (approximate)
                    loop_size = i - loop_start
                    if loop_size > self.config.large_loop_threshold:
                        return True
                    in_loop = False

            return False
        except Exception:
            return False

    def calculate_complexity_score(
        self,
        loc: int,
        loops: int,
        has_nested: bool,
        has_deep: bool,
        has_large: bool
    ) -> float:
"""
Calculate a complexity score for prioritization.""
score = (loops * 2) + (loc / 100)

        if has_nested:
            score *= 1.5
        if has_deep:
            score *= 2.0
        if has_large:
            score *= 1.8

        return round(score, 2)

    def analyze_file(self, file_path: str) -> LoopAnalysisResult:
"""
Analyze a single file for loop anti-patterns.""
loc = self.count_lines(file_path)
        loops = self.count_loops_ripgrep(file_path)
        has_nested, has_deep = self.analyze_nesting(file_path)
        has_large = self.analyze_loop_sizes(file_path)

        density = (loops / max(loc, 1)) * 100
        complexity = self.calculate_complexity_score(
            loc, loops, has_nested, has_deep, has_large
        )

        return LoopAnalysisResult(
            file_path=file_path,
            lines_of_code=loc,
            loop_count=loops,
            complexity_score=complexity,
            loop_density=round(density, 2),
            has_nested_loops=has_nested,
            has_deep_nesting=has_deep,
            has_large_loops=has_large
        )

    def should_analyze_file(self, file_path: str) -> bool:
"""
Check if a file should be analyzed based on config.""
# Check exclude directories
        path_parts = Path(file_path).parts
        if any(excl_dir in path_parts for excl_dir in self.config.exclude_dirs):
            return False

        # Check file extensions
        file_name = os.path.basename(file_path)
        if not any(
            file_name.endswith(ext.lstrip('*'))'            for ext in self.config.include_patterns
        ):
            return False

        # Check exclude patterns
        for pattern in self.config.exclude_patterns:
            if re.search(pattern, file_path):
                return False

        return True

    def find_candidates(self, root_dir: str) -> List[LoopAnalysisResult]:
"""
Find files that are candidates for loop optimization.""
candidates = []

        for root, dirs, files in os.walk(root_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

            for file in files:
                file_path = os.path.join(root, file)

                if not self.should_analyze_file(file_path):
                    continue

                result = self.analyze_file(file_path)

                # Apply thresholds
                if (
                        result.lines_of_code >= self.config.min_loc_threshold
                        and result.loop_count >= self.config.min_loop_threshold
                ):
                    candidates.append(result)

        # Sort by complexity score (highest first)
        return sorted(candidates, key=lambda x: x.complexity_score, reverse=True)

    def analyze_directory(self, root_dir: str) -> Dict[str, List[LoopAnalysisResult]]:
"""
Comprehensive analysis of a directory.""
all_files = []
        candidates = []

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

            for file in files:
                file_path = os.path.join(root, file)

                if not self.should_analyze_file(file_path):
                    continue

                result = self.analyze_file(file_path)
                all_files.append(result)

                if (
                        result.lines_of_code >= self.config.min_loc_threshold and
                        result.loop_count >= self.config.min_loop_threshold
                ):
                    candidates.append(result)

        return {
            'all_files': sorted(all_files, key=lambda x: x.complexity_score, reverse=True),'            'candidates': sorted(candidates, key=lambda x: x.complexity_score, reverse=True)'        }


def print_analysis_report(results: List[LoopAnalysisResult], title: str = "Loop Analysis Report"):"    """
Print a formatted analysis report.""
print(f"\\n{title}")"    print("=" * len(title))"
    if not results:
        print("No files found matching criteria.")"        return

    print(f"Found {len(results)} files:")"    print()

    for result in results[:20]:  # Show top 20
        flags = []
        if result.has_nested_loops:
            flags.append("NESTED")"        if result.has_deep_nesting:
            flags.append("DEEP")"        if result.has_large_loops:
            flags.append("LARGE")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
print(f" {result.file_path}")"        print(f"   LOC: {result.lines_of_code}, Loops: {result.loop_count}, ""              f"Density: {result.loop_density:.1f}%, Score: {result.complexity_score}{flag_str}")"        print()


# CLI interface for reuse across fleet
if __name__ == "__main__":"    import argparse

    parser = argparse.ArgumentParser(description="PyAgent Loop Analysis Utility")"    parser.add_argument("directory", help="Directory to analyze")"    parser.add_argument("--min-loc", type=int, default=200, help="Minimum lines of code threshold")"    parser.add_argument("--min-loops", type=int, default=3, help="Minimum loop count threshold")"    parser.add_argument(
        "--exclude", nargs='*', default=['.venv', '__pycache__', 'node_modules'],"'        help="Directories to exclude""    )
    parser.add_argument(
        "--format", choices=['summary', 'detailed'], default='summary',"'        help="Output format""    )

    args = parser.parse_args()

    config = LoopAnalysisConfig(
        min_loc_threshold=args.min_loc,
        min_loop_threshold=args.min_loops,
        exclude_dirs=set(args.exclude)
    )

    analyzer = LoopAnalyzer(config)
    results = analyzer.find_candidates(args.directory)

    if args.format == 'detailed':'        analysis = analyzer.analyze_directory(args.directory)
        print_analysis_report(analysis['candidates'], "High Priority Candidates")"'        print_analysis_report(analysis['all_files'][:10], "Top 10 Files by Complexity")"'    else:
        print_analysis_report(results, "Loop Analysis Summary")
"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
