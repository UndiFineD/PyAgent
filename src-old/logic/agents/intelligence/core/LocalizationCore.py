"""LLM_CONTEXT_START

## Source: src-old/logic/agents/intelligence/core/LocalizationCore.description.md

# LocalizationCore

**File**: `src\\logic\agents\\intelligence\\core\\LocalizationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 53  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LocalizationCore.

## Classes (1)

### `LocalizationCore`

LocalizationCore handles translation logic (placeholder) and Cultural Guardrails.
It identifies problematic idioms or metaphors in multi-agent communication.

**Methods** (4):
- `__init__(self)`
- `detect_cultural_issues(self, text)`
- `get_supported_locales(self)`
- `format_translation_request(self, text, target_lang)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/intelligence/core/LocalizationCore.improvements.md

# Improvements for LocalizationCore

**File**: `src\\logic\agents\\intelligence\\core\\LocalizationCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 53 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LocalizationCore_test.py` with pytest tests

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

import re
from typing import Any


class LocalizationCore:
    """LocalizationCore handles translation logic (placeholder) and Cultural Guardrails.
    It identifies problematic idioms or metaphors in multi-agent communication.
    """

    def __init__(self) -> None:
        # List of potentially offensive or culturally insensitive metaphors/idioms
        # This is a basic starter list for the guardrail.
        self.cultural_red_flags = [
            r"\bbite the bullet\b",  # Violent metaphor
            r"\bkill two birds\b",  # Violent metaphor
            r"\bdoghouse\b",  # Culturally variable idiom
            r"\bgrandfathered\b",  # Potentially non-inclusive language
            r"\bblackbox\b",  # Potentially non-inclusive language
            r"\bwhitelist\b",  # Potentially non-inclusive language
            r"\bblacklist\b",  # Potentially non-inclusive language
            r"\bsanity check\b",  # Potentially ableist language
        ]

    def detect_cultural_issues(self, text: str) -> list[dict[str, Any]]:
        """Detects cultural red flags in agent communication.
        Returns a list of identified issues with suggestions.
        """
        issues = []
        for pattern in self.cultural_red_flags:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append(
                    {
                        "term": match.group(),
                        "index": match.start(),
                        "severity": "low",
                        "suggestion": "Consider more direct or inclusive technical language.",
                    }
                )
        return issues

    def get_supported_locales(self) -> list[str]:
        """Returns the 12 major languages currently prioritized for translation."""
        return ["en", "zh", "es", "hi", "ar", "bn", "pt", "ru", "ja", "de", "fr", "ko"]

    def format_translation_request(self, text: str, target_lang: str) -> str:
        """Constructs a prompt or request for an external translation service (DeepL/LLM)."""
        return f"Translate the following technical agent comment to {target_lang}:\n\n{text}"
