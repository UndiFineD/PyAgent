#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/agent/NotificationCore.description.md

# NotificationCore

**File**: `src\classes\agent\NotificationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 39  
**Complexity**: 3 (simple)

## Overview

NotificationCore logic for PyAgent.
Pure logic for payload formatting and domain extraction.
No I/O or side effects.

## Classes (1)

### `NotificationCore`

Pure logic core for notification management.

**Methods** (3):
- `construct_payload(event_name, event_data)`
- `get_domain_from_url(url)`
- `validate_event_data(data)`

## Dependencies

**Imports** (5):
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/NotificationCore.improvements.md

# Improvements for NotificationCore

**File**: `src\classes\agent\NotificationCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 39 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NotificationCore_test.py` with pytest tests

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

"""
NotificationCore logic for PyAgent.
Pure logic for payload formatting and domain extraction.
No I/O or side effects.
"""

import time
import urllib.parse
from typing import Dict, Any, Optional


class NotificationCore:
    """Pure logic core for notification management."""

    @staticmethod
    def construct_payload(
        event_name: str, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Formats the JSON payload for webhook delivery."""
        return {
            "event": event_name,
            "timestamp": time.time(),
            "data": event_data,
            "version": "1.1.0",
        }

    @staticmethod
    def get_domain_from_url(url: str) -> str:
        """Extracts the network location (domain) from a URL for connectivity tracking."""
        try:
            domain = urllib.parse.urlparse(url).netloc
            return domain or url
        except Exception:
            return url

    @staticmethod
    def validate_event_data(data: Dict[str, Any]) -> bool:
        """Basic validation for event data structures."""
        # Ensure it's a non-empty dictionary
        return isinstance(data, dict) and len(data) > 0
