#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/CoderValidationMixin.description.md

# CoderValidationMixin

**File**: `src\\logic\agents\\development\\mixins\\CoderValidationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 66  
**Complexity**: 2 (simple)

## Overview

Syntax validation and linting logic for CoderCore.

## Classes (1)

### `CoderValidationMixin`

Mixin for validating syntax and linting code.

**Methods** (2):
- `validate_syntax(self, content)`
- `validate_flake8(self, content)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `ast`
- `logging`
- `os`
- `shutil`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `subprocess`
- `tempfile`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/CoderValidationMixin.improvements.md

# Improvements for CoderValidationMixin

**File**: `src\\logic\agents\\development\\mixins\\CoderValidationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 66 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoderValidationMixin_test.py` with pytest tests

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

"""
Syntax validation and linting logic for CoderCore.
"""

import ast
import logging
import os
import shutil
import subprocess
import tempfile

from src.core.base.types.CodeLanguage import CodeLanguage


class CoderValidationMixin:
    """Mixin for validating syntax and linting code."""

    def validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if self.language != CodeLanguage.PYTHON:
            return True
        try:
            ast.parse(content)
            return True
        except (SyntaxError, RecursionError, MemoryError) as e:
            logging.error(f"Syntax error in generated code: {e}")
            return False

    def validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if self.language != CodeLanguage.PYTHON:
            return True
        if not shutil.which("flake8"):
            logging.warning("flake8 not found, skipping style validation")
            return True
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            # Run flake8 on the temporary file
            result = subprocess.run(
                ["flake8", "--ignore=E501,F401,W291,W293", tmp_path],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0
        except Exception as e:
            logging.error(f"flake8 validation failed: {e}")
            return True
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
