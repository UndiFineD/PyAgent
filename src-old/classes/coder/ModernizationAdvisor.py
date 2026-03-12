#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/ModernizationAdvisor.description.md

# ModernizationAdvisor

**File**: `src\classes\coder\ModernizationAdvisor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 83  
**Complexity**: 2 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `ModernizationAgent`

Advises on modernizing deprecated APIs.

Tracks deprecated API usage and suggests modern replacements.

Attributes:
    suggestions: List of modernization suggestions.

Example:
    >>> advisor=ModernizationAgent()
    >>> suggestions=advisor.analyze("import urllib2")

**Methods** (2):
- `__init__(self)`
- `analyze(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.types.ModernizationSuggestion.ModernizationSuggestion`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/ModernizationAdvisor.improvements.md

# Improvements for ModernizationAdvisor

**File**: `src\classes\coder\ModernizationAdvisor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 83 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ModernizationAdvisor_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_coder.py"""

from src.core.base.version import VERSION
from src.core.base.types.ModernizationSuggestion import ModernizationSuggestion
from typing import List, Optional, Tuple
import re

__version__ = VERSION


class ModernizationAgent:
    """Advises on modernizing deprecated APIs.

    Tracks deprecated API usage and suggests modern replacements.

    Attributes:
        suggestions: List of modernization suggestions.

    Example:
        >>> advisor=ModernizationAgent()
        >>> suggestions=advisor.analyze("import urllib2")
    """

    DEPRECATIONS: list[tuple[str, str, str, str | None, str]] = [
        (
            r"import\s+urllib2",
            "urllib.request",
            "2.7",
            "3.0",
            "https://docs.python.org/3/library/urllib.request.html",
        ),
        (
            r"from\s+collections\s+import\s+.*\bMapping\b",
            "collections.abc.Mapping",
            "3.3",
            "3.10",
            "Use collections.abc instead of collections for ABCs",
        ),
        (
            r'\.encode\s*\(\s*[\'"]hex[\'"]\s*\)',
            "binascii.hexlify()",
            "3.0",
            None,
            "Use binascii.hexlify() instead of .encode('hex')",
        ),
        (
            r"asyncio\.get_event_loop\(\)",
            "asyncio.get_running_loop() or asyncio.new_event_loop()",
            "3.10",
            None,
            "get_event_loop() deprecated in favor of more explicit alternatives",
        ),
    ]

    def __init__(self) -> None:
        """Initialize the modernization advisor."""
        self.suggestions: list[ModernizationSuggestion] = []

    def analyze(self, content: str) -> list[ModernizationSuggestion]:
        """Analyze code for deprecated API usage.

        Args:
            content: Source code to analyze.

        Returns:
            List of modernization suggestions.
        """
        self.suggestions = []

        for pattern, new_api, dep_ver, rem_ver, guide in self.DEPRECATIONS:
            if re.search(pattern, content):
                self.suggestions.append(
                    ModernizationSuggestion(
                        old_api=pattern,
                        new_api=new_api,
                        deprecation_version=dep_ver,
                        removal_version=rem_ver,
                        migration_guide=guide,
                    )
                )

        return self.suggestions
