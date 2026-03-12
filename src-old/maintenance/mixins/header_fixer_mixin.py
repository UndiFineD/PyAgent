#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/maintenance/mixins/header_fixer_mixin.description.md

# header_fixer_mixin

**File**: `src\maintenance\mixins\header_fixer_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 120  
**Complexity**: 1 (simple)

## Overview

Mixin for fixing license headers and docstring placement.

## Classes (1)

### `HeaderFixerMixin`

Provides automated fixes for license headers and __future__ imports.

**Methods** (1):
- `clean_file_headers(self, file_path)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `logging`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/maintenance/mixins/header_fixer_mixin.improvements.md

# Improvements for header_fixer_mixin

**File**: `src\maintenance\mixins\header_fixer_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 120 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `header_fixer_mixin_test.py` with pytest tests

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

"""
Mixin for fixing license headers and docstring placement.
"""


import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HeaderFixerMixin:
    """Provides automated fixes for license headers and __future__ imports."""

    def clean_file_headers(self, file_path: Path) -> bool:
        """Remove duplicate license headers and docstrings, fix __future__ positioning.
        Salvaged from temp fix scripts.
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            result = []
            in_first_docstring = False
            docstring_count = 0
            seen_copyright = False

            i = 0
            while i < len(lines):
                line = lines[i]

                # Keep shebang and copyright header
                if line.startswith("#!") or (
                    line.startswith("#") and "Copyright" in line
                ):
                    result.append(line)
                    if "Copyright" in line:
                        seen_copyright = True
                    i += 1
                    continue

                # Skip other header comments for now, keep actual content
                if line.startswith("#") and not any(
                    x in line for x in ["pylint", "noqa", "type:"]
                ):
                    if seen_copyright and any(
                        x in line for x in ["Without", "See the", "limitations"]
                    ):
                        # This is likely part of a duplicate license block
                        pass
                    elif not seen_copyright:
                        result.append(line)
                    else:
                        # Likely a normal comment or a repeat
                        result.append(line)
                    i += 1
                    continue

                # Handle docstrings - keep only the first one
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    if docstring_count == 0:
                        in_first_docstring = True
                        docstring_count += 1
                        result.append(line)
                    elif in_first_docstring:
                        result.append(line)
                        if (
                            line.strip().endswith('"""') or line.strip().endswith("'''")
                        ) and len(line.strip()) > 3:
                            in_first_docstring = False
                    i += 1
                    continue

                # Add non-duplicate content
                if not in_first_docstring or docstring_count == 0:
                    result.append(line)

                i += 1

            # Ensure __future__ imports come after docstring
            final_lines = []
            future_imports = []
            docstring_done = False

            for line in result:
                if '"""' in line or "'''" in line:
                    final_lines.append(line)
                    if line.strip().count('"""') >= 1 or line.strip().count("'''") >= 1:
                        # Simple detection for end of docstring
                        if line.strip().endswith('"""') or line.strip().endswith("'''"):
                            docstring_done = True
                elif line.strip().startswith("from __future__"):
                    if not docstring_done:
                        future_imports.append(line)
                    else:
                        final_lines.append(line)
                else:
                    if (
                        future_imports
                        and not line.strip().startswith("from __future__")
                        and line.strip()
                    ):
                        final_lines.extend(future_imports)
                        future_imports = []
                        docstring_done = True
                    final_lines.append(line)

            if future_imports:
                final_lines.extend(future_imports)

            new_content = "\n".join(final_lines)
            if new_content != content:
                file_path.write_text(new_content, encoding="utf-8")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to fix headers in {file_path}: {e}")
            return False
