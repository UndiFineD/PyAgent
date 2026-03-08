#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/CoderLanguageMixin.description.md

# CoderLanguageMixin

**File**: `src\logic\agents\development\mixins\CoderLanguageMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 61  
**Complexity**: 6 (moderate)

## Overview

Language detection and validation logic for CoderAgent.

## Classes (1)

### `CoderLanguageMixin`

Mixin for code language detection and syntax validation.

**Methods** (6):
- `_detect_language(self)`
- `detect_language(self)`
- `language(self)`
- `_is_python_file(self)`
- `_validate_syntax(self, content)`
- `_validate_flake8(self, content)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.core.base.types.CodeLanguage.CodeLanguage`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/CoderLanguageMixin.improvements.md

# Improvements for CoderLanguageMixin

**File**: `src\logic\agents\development\mixins\CoderLanguageMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 61 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoderLanguageMixin_test.py` with pytest tests

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

"""Language detection and validation logic for CoderAgent."""

from src.core.base.types.CodeLanguage import CodeLanguage

class CoderLanguageMixin:
    """Mixin for code language detection and syntax validation."""

    def _detect_language(self) -> CodeLanguage:
        """Detect the programming language from file extension."""
        if not hasattr(self, "file_path"):
            return CodeLanguage.UNKNOWN
        ext = self.file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, CodeLanguage.UNKNOWN)

    def detect_language(self) -> CodeLanguage:
        """Public wrapper to detect and return the file language.

        Returns:
            The detected CodeLanguage based on file extension.
        """
        self._language = self._detect_language()
        if hasattr(self, "core"):
            self.core.language = self._language  # Sync core
        return self._language

    @property
    def language(self) -> CodeLanguage:
        """Get the detected language."""
        return getattr(self, "_language", CodeLanguage.UNKNOWN)

    @property
    def _is_python_file(self) -> bool:
        """Check if the file is a Python file."""
        return self.language == CodeLanguage.PYTHON

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if hasattr(self, "core"):
            return self.core.validate_syntax(content)
        return True

    def _validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if hasattr(self, "core"):
            return self.core.validate_flake8(content)
        return True
