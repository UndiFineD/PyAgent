#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/utils.description.md

# utils

**File**: `src\classes\stats\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 7 imports  
**Lines**: 80  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for utils.

## Functions (1)

### `main()`

CLI entry point for the Stats Agent.

## Dependencies

**Imports** (7):
- `StatsAgent.StatsAgent`
- `argparse`
- `json`
- `logging`
- `matplotlib`
- `matplotlib.pyplot`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/classes/stats/utils.improvements.md

# Improvements for utils

**File**: `src\classes\stats\utils.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `utils_test.py` with pytest tests

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

import argparse
import json
import logging
import sys

try:
    import matplotlib
    # Use non-interactive backend
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    has_matplotlib = True
except (ImportError, RuntimeError, Exception):
    plt = None
    has_matplotlib = False

from .StatsAgent import StatsAgent

def main() -> None:
    """CLI entry point for the Stats Agent."""
    parser = argparse.ArgumentParser(
        description='Stats Agent: Reports file update statistics',
        epilog='Example: python src/agent_stats.py --files src/*.py'
    )
    parser.add_argument('--files', nargs='+', required=True, help='List of files to analyze')
    parser.add_argument(
        '--format',
        choices=[
            'text',
            'json',
            'csv'],
        default='text',
        help='Output format')
    parser.add_argument('--coverage', help='Path to code coverage report')
    parser.add_argument('--export', nargs='+', help='Export formats (json, csv, html, sqlite)')
    parser.add_argument('--baseline', help='Path to baseline stats for comparison')
    parser.add_argument('--verbose', default='normal', help='Verbosity level')
    parser.add_argument('--no-cascade', action='store_true', help='Unused, for compatibility')
    args = parser.parse_args()

    # Setup logging
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
    }
    level = levels.get(args.verbose.lower(), logging.INFO)
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        agent = StatsAgent(args.files)
        if args.coverage:
            agent.track_code_coverage(args.coverage)
        if args.export:
            agent.export_stats('stats_output', args.export)
        if args.baseline:
            with open(args.baseline, 'r') as baseline_file:
                baseline_stats = json.load(baseline_file)
            agent.generate_comparison_report(baseline_stats)
        agent.report_stats(output_format=args.format)
        if has_matplotlib:
            agent.visualize_stats()
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
