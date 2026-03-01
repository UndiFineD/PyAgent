# loop_analyzer

**File**: `src\core\specialists\loop_analyzer.py`  
**Type**: Python Module  
**Summary**: 3 classes, 1 functions, 11 imports  
**Lines**: 339  
**Complexity**: 13 (moderate)

## Overview

Loop Analysis Utility for PyAgent Fleet

This module provides reusable utilities for analyzing and detecting
anti-patterns related to for/while loops across the PyAgent codebase.
Used for performance profiling and code quality assessment.

## Classes (3)

### `LoopAnalysisResult`

Result of loop analysis for a single file.

### `LoopAnalysisConfig`

Configuration for loop analysis.

**Methods** (1):
- `__post_init__(self)`

### `LoopAnalyzer`

Reusable analyzer for detecting loop anti-patterns.

**Methods** (11):
- `__init__(self, config)`
- `count_loops_ripgrep(self, file_path)`
- `_count_loops_regex(self, file_path)`
- `count_lines(self, file_path)`
- `analyze_nesting(self, file_path)`
- `analyze_loop_sizes(self, file_path)`
- `calculate_complexity_score(self, loc, loops, has_nested, has_deep, has_large)`
- `analyze_file(self, file_path)`
- `should_analyze_file(self, file_path)`
- `find_candidates(self, root_dir)`
- ... and 1 more methods

## Functions (1)

### `print_analysis_report(results, title)`

Print a formatted analysis report.

## Dependencies

**Imports** (11):
- `argparse`
- `dataclasses.dataclass`
- `os`
- `pathlib.Path`
- `re`
- `subprocess`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
