#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/IdiomExtractorAgent.description.md

# IdiomExtractorAgent

**File**: `src\classes\specialized\IdiomExtractorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 104  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for IdiomExtractorAgent.

## Classes (1)

### `IdiomExtractorAgent`

**Inherits from**: BaseAgent

Agent responsible for extracting project-specific coding idioms and patterns.
Maintains a .pyagent_idioms.json file to guide future code generation.

**Methods** (3):
- `__init__(self, file_path)`
- `extract_idioms(self, directory)`
- `get_current_idioms(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/IdiomExtractorAgent.improvements.md

# Improvements for IdiomExtractorAgent

**File**: `src\classes\specialized\IdiomExtractorAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 104 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `IdiomExtractorAgent_test.py` with pytest tests

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

import json
import logging
import os
import re
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

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
from src.core.base.version import VERSION

__version__ = VERSION


class IdiomExtractorAgent(BaseAgent):
    """Agent responsible for extracting project-specific coding idioms and patterns.
    Maintains a .pyagent_idioms.json file to guide future code generation.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.idioms_file = ".pyagent_idioms.json"

    @as_tool
    def extract_idioms(self, directory: str = "src") -> str:
        """Scans the specified directory for coding patterns and updates the idioms library.
        """
        logging.info(f"IdiomExtractor: Scanning {directory} for idioms...")

        idioms = {
            "naming_conventions": {
                "classes": "PascalCase",
                "functions": "snake_case",
                "variables": "snake_case",
            },
            "common_decorators": [],
            "frequent_imports": [],
            "error_handling_patterns": [],
            "docstring_style": "Google",
        }

        # Simple pattern extraction logic
        decorator_pattern = re.compile(r"@([a-zA-Z0-9_\.]+)")
        import_pattern = re.compile(r"^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)")

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), encoding="utf-8") as f:
                            content = f.read()

                            # Extract decorators
                            found_decorators = decorator_pattern.findall(content)
                            idioms["common_decorators"].extend(found_decorators)

                            # Extract common imports
                            found_imports = import_pattern.findall(content)
                            idioms["frequent_imports"].extend(found_imports)

                            # Check for docstring styles
                            if '"""' in content and ":" in content:
                                if "Args:" in content or "Returns:" in content:
                                    idioms["docstring_style"] = "Google"
                                elif ":param" in content:
                                    idioms["docstring_style"] = "reStructuredText"

                    except Exception as e:
                        logging.warning(f"Error reading {file}: {e}")

        # Deduplicate and sort
        idioms["common_decorators"] = sorted(list(set(idioms["common_decorators"])))
        idioms["frequent_imports"] = sorted(list(set(idioms["frequent_imports"])))[
            :50
        ]  # Top 50

        # Save to file
        with open(self.idioms_file, "w", encoding="utf-8") as f:
            json.dump(idioms, f, indent=4)

        return f"Successfully extracted {len(idioms['common_decorators'])} decorators and {len(idioms['frequent_imports'])} common imports. Saved to {self.idioms_file}."

    @as_tool
    def get_current_idioms(self) -> dict[str, Any]:
        """Returns the currently stored project idioms.
        """
        if os.path.exists(self.idioms_file):
            with open(self.idioms_file, encoding="utf-8") as f:
                return json.load(f)
        return {"error": "Idioms file not found. Run extract_idioms first."}
