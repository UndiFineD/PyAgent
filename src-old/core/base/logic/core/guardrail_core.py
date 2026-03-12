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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/guardrail_core.description.md

# guardrail_core

**File**: `src\\core\base\\logic\\core\\guardrail_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for guardrail_core.

## Classes (1)

### `GuardrailCore`

Implements output validation and logical checks for agent tasks.
Harvested from agentic-design-patterns.

**Methods** (3):
- `validate_pydantic(output, model)`
- `apply_logical_check(data, check_func)`
- `moderate_content(text, forbidden_keywords)`

## Dependencies

**Imports** (10):
- `json`
- `logging`
- `pydantic.BaseModel`
- `pydantic.ValidationError`
- `re`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`
- `typing.Tuple`
- `typing.Type`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/guardrail_core.improvements.md

# Improvements for guardrail_core

**File**: `src\\core\base\\logic\\core\\guardrail_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `guardrail_core_test.py` with pytest tests

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

import json
import re
from typing import Any, Callable, Optional, Tuple, Type

from pydantic import BaseModel, ValidationError


class GuardrailCore:
    """Implements output validation and logical checks for agent tasks.
    Harvested from agentic-design-patterns.
    """

    @staticmethod
    def validate_pydantic(
        output: str, model: Type[BaseModel]
    ) -> Tuple[bool, Any, Optional[str]]:
        """Validates that output matches a Pydantic model."""
        try:
            # Attempt to parse json
            data = json.loads(output)
            validated = model.model_validate(data)
            return True, validated, None
        except (json.JSONDecodeError, ValidationError) as e:
            return False, None, str(e)

    @staticmethod
    def apply_logical_check(
        data: Any, check_func: Callable[[Any], Tuple[bool, str]]
    ) -> Tuple[bool, str]:
        """Applies a custom logical check function to validated data."""
        return check_func(data)

    @staticmethod
    def moderate_content(text: str, forbidden_keywords: list[str]) -> Tuple[bool, str]:
        """Simple keyword-based moderation."""
        pattern = r"\b(" + "|".join(re.escape(k) for k in forbidden_keywords) + r")\b"
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Content contains forbidden keywords."
        return True, "Content is clean."
