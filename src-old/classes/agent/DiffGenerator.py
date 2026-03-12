#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent/DiffGenerator.description.md

# DiffGenerator

**File**: `src\\classes\agent\\DiffGenerator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 178  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `DiffGenerator`

Generates diffs to preview changes before applying them.

Creates human - readable diffs in various formats to allow
users to review changes before they are applied.

Attributes:
    output_format: Default output format for diffs.
    context_lines: Number of context lines in diff.

**Methods** (4):
- `__init__(self, output_format, context_lines)`
- `generate_diff(self, file_path, original, modified)`
- `format_diff(self, diff_result, output_format)`
- `print_diff(self, diff_result)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `difflib`
- `pathlib.Path`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.core.base.models.DiffOutputFormat`
- `src.core.base.models.DiffResult`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/DiffGenerator.improvements.md

# Improvements for DiffGenerator

**File**: `src\\classes\agent\\DiffGenerator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 178 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DiffGenerator_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

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


"""Auto-extracted class from agent.py"""

import difflib
import sys
from pathlib import Path

from src.core.base.models import DiffOutputFormat, DiffResult
from src.core.base.Version import VERSION

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class DiffGenerator:
    """Generates diffs to preview changes before applying them.

    Creates human - readable diffs in various formats to allow
    users to review changes before they are applied.

    Attributes:
        output_format: Default output format for diffs.
        context_lines: Number of context lines in diff.

    """

    def __init__(
        self,
        output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED,
        context_lines: int = 3,
    ) -> str:
        """Initialize the diff generator.

        Args:
            output_format: Default output format.
            context_lines: Number of context lines.

        """
        self.output_format = output_format
        self.context_lines = context_lines

    def generate_diff(
        self, file_path: Path, original: str, modified: str
    ) -> DiffResult:
        """Generate a diff between original and modified content.

        Args:
            file_path: Path to the file.
            original: Original file content.
            modified: Modified content.

        Returns:
            DiffResult with diff information.

        """
        # Rust-accelerated diff generation
        if HAS_RUST:
            try:
                diff_text, additions, deletions = rc.generate_unified_diff_rust(
                    original, modified, file_path.name, self.context_lines
                )  # type: ignore[attr-defined]
                diff_lines = diff_text.splitlines(keepends=True)
                return DiffResult(
                    file_path=file_path,
                    original_content=original,
                    modified_content=modified,
                    diff_lines=diff_lines,
                    additions=additions,
                    deletions=deletions,
                    changes=additions + deletions,
                )
            except Exception:
                pass

        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        # Generate unified diff
        diff_lines = list(
            difflib.unified_diff(
                original_lines,
                modified_lines,
                fromfile=f"a/{file_path.name}",
                tofile=f"b/{file_path.name}",
                n=self.context_lines,
            )
        )

        # Count additions and deletions
        additions = sum(
            1
            for line in diff_lines
            if line.startswith("+") and not line.startswith("+++")
        )
        deletions = sum(
            1
            for line in diff_lines
            if line.startswith("-") and not line.startswith("---")
        )

        return DiffResult(
            file_path=file_path,
            original_content=original,
            modified_content=modified,
            diff_lines=diff_lines,
            additions=additions,
            deletions=deletions,
            changes=additions + deletions,
        )

    def format_diff(
        self, diff_result: DiffResult, output_format: DiffOutputFormat | None = None
    ) -> str:
        """Format a diff result for display.

        Args:
            diff_result: DiffResult to format.
            output_format: Output format (uses default if not provided).

        Returns:
            Formatted diff string.

        """
        fmt = output_format or self.output_format

        if fmt == DiffOutputFormat.UNIFIED:
            return "".join(diff_result.diff_lines)
        elif fmt == DiffOutputFormat.CONTEXT:
            original = diff_result.original_content.splitlines(keepends=True)
            modified = diff_result.modified_content.splitlines(keepends=True)
            return "".join(
                difflib.context_diff(
                    original,
                    modified,
                    fromfile=f"a/{diff_result.file_path.name}",
                    tofile=f"b/{diff_result.file_path.name}",
                    n=self.context_lines,
                )
            )
        elif fmt == DiffOutputFormat.HTML:
            differ = difflib.HtmlDiff()
            original = diff_result.original_content.splitlines()
            modified = diff_result.modified_content.splitlines()
            return differ.make_file(original, modified)
        else:
            return "".join(diff_result.diff_lines)

    def print_diff(self, diff_result: DiffResult) -> None:
        """Print a colorized diff to console.

        Args:
            diff_result: DiffResult to print.

        """
        for line in diff_result.diff_lines:
            if line.startswith("+") and not line.startswith("+++"):
                sys.stdout.write(f"\033[92m{line}\033[0m")  # Green
            elif line.startswith("-") and not line.startswith("---"):
                sys.stdout.write(f"\033[91m{line}\033[0m")  # Red
            elif line.startswith("@@"):
                sys.stdout.write(f"\033[96m{line}\033[0m")  # Cyan
            else:
                sys.stdout.write(line)
        sys.stdout.flush()
