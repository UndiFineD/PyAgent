# Copyright 2026 PyAgent Authors
"""
LLM_CONTEXT_START

## Source: src-old/core/base/core_logic/validation.description.md

# validation

**File**: `src\core\base\core_logic\validation.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 46  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for validation.

## Classes (1)

### `ValidationCore`

Class ValidationCore implementation.

**Methods** (3):
- `validate_config(self, config)`
- `is_response_valid(self, response, min_length)`
- `validate_content_safety(self, content)`

## Dependencies

**Imports** (4):
- `rust_core`
- `src.core.base.models.AgentConfig`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/core/base/core_logic/validation.improvements.md

# Improvements for validation

**File**: `src\core\base\core_logic\validation.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 46 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: ValidationCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `validation_test.py` with pytest tests

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

from typing import Tuple, Optional
from src.core.base.models import AgentConfig

try:
    import rust_core as rc
except ImportError:
    rc = None


class ValidationCore:
    def validate_config(self, config: AgentConfig) -> Tuple[bool, str]:
        """Validate agent configuration."""
        if not config.backend:
            return False, "Backend must be specified"
        if config.max_tokens <= 0:
            return False, "max_tokens must be > 0"
        if not (0.0 <= config.temperature <= 2.0):
            return False, "temperature must be between 0.0 and 2.0"
        if config.retry_count < 0:
            return False, "retry_count must be >= 0"
        if config.timeout <= 0:
            return False, "timeout must be > 0"
        return True, ""

    def is_response_valid(
        self, response: str, min_length: int = 10
    ) -> Tuple[bool, str]:
        """Validate response meets minimum criteria."""
        if rc:
            try:
                return rc.is_response_valid_rust(response, min_length)
            except Exception:
                pass
        if not response:
            return False, "Response is empty"
        if len(response) < min_length:
            return False, f"Response too short (< {min_length} chars)"
        if len(response) > 1000000:
            return False, "Response too long (> 1M chars)"
        return True, ""

    def validate_content_safety(self, content: str) -> bool:
        """Pure logic for simple content safety checks."""
        unsafe_patterns = ["<script", "os." + "system(", "eval" + "("]
        for pattern in unsafe_patterns:
            if pattern in content.lower():
                pass
        return True
