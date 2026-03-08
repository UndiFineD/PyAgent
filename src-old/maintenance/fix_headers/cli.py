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

"""
LLM_CONTEXT_START

## Source: src-old/maintenance/fix_headers/cli.description.md

# cli

**File**: `src\maintenance\fix_headers\cli.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 74  
**Complexity**: 1 (simple)

## Overview

CLI interface for the Fix Headers Tool.

## Functions (1)

### `main()`

CLI entry point for the Fix Headers Tool.

## Dependencies

**Imports** (3):
- `argparse`
- `fix_headers_agent.FixHeadersAgent`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/maintenance/fix_headers/cli.improvements.md

# Improvements for cli

**File**: `src\maintenance\fix_headers\cli.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 74 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `cli_test.py` with pytest tests

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

"""
CLI interface for the Fix Headers Tool.
"""

import sys
import argparse

from .fix_headers_agent import FixHeadersAgent


def main():
    """CLI entry point for the Fix Headers Tool."""
    parser = argparse.ArgumentParser(
        description="Fix Apache 2.0 headers in Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.maintenance.fix_headers.cli src/logic/agents/
  python -m src.maintenance.fix_headers.cli --dry-run --verbose src/
  python -m src.maintenance.fix_headers.cli single_file.py

This tool ensures all Python files have proper Apache 2.0 license headers
with PyAgent copyright notices.
        """
    )

    parser.add_argument(
        'target',
        help='File or directory to process'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Provide detailed output for each file'
    )

    parser.add_argument(
        '--exclude',
        action='append',
        help='Directory patterns to exclude (can be used multiple times)'
    )

    args = parser.parse_args()

    exclude_patterns = set(args.exclude or [])
    exclude_patterns.update({'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'})

    agent = FixHeadersAgent(dry_run=args.dry_run, verbose=args.verbose)
    agent.run(args.target, exclude_patterns)


if __name__ == "__main__":
    main()