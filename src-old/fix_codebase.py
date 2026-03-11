#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/fix_codebase.description.md

# fix_codebase

**File**: `src\fix_codebase.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 4 imports  
**Lines**: 57  
**Complexity**: 1 (simple)

## Overview

Utility to repair corrupted source files by uncommenting essential system imports.
Part of the Fleet Healer autonomous recovery pattern.

## Functions (1)

### `uncomment_lines(root_dir)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `os`
- `re`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/fix_codebase.improvements.md

# Improvements for fix_codebase

**File**: `src\fix_codebase.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 57 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_codebase_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Utility to repair corrupted source files by uncommenting essential system imports.
Part of the Fleet Healer autonomous recovery pattern.
"""

import os
import re

from src.core.base.version import VERSION

__version__ = VERSION


def uncomment_lines(root_dir: str) -> None:
    # Regex to catch commented-out essential imports
    p_from = re.compile(
        r"^\s*#\s*(from\s+(?:typing|dataclasses|__future__|pathlib|datetime|abc|functools|enum|typing_extensions)\s+import\s+)",
        re.M,
    )
    p_import = re.compile(
        r"^\s*#\s*(import\s+(?:os|json|logging|re|sys|time|math|hashlib|shutil|subprocess|tempfile|glob|uuid|collections|random|inspect|threading|queue|socket|urllib|traceback|ast|argparse|pathlib))\b",
        re.M,
    )

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()

                    new_content = p_from.sub(r"\1", content)
                    new_content = p_import.sub(r"\1", new_content)

                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Fixed: {filepath}")
                except Exception as e:
                    print(f"Error fixing {filepath}: {e}")


if __name__ == "__main__":
    uncomment_lines("src/classes")
