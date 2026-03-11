"""LLM_CONTEXT_START

## Source: src-old/version.description.md

# version

**File**: `src\version.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 0 imports  
**Lines**: 14  
**Complexity**: 1 (simple)

## Overview

PyAgent SDK Version Info and Stability Gates.

## Functions (1)

### `is_gate_open(required_phase)`

Gatekeeping: Returns True if the system maturity allows for the required phase.

---
*Auto-generated documentation*
## Source: src-old/version.improvements.md

# Improvements for version

**File**: `src\version.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 14 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `version_test.py` with pytest tests

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

"""
PyAgent SDK Version Info and Stability Gates.
"""

# PyAgent SDK Version Info (Core/Fleet Version)
VERSION = "2.1.5-stable"
SDK_VERSION = "3.1.0"
EVOLUTION_PHASE = 116
STABILITY_SCORE = (
    1.0  # Phase 108: Multi-Agent Logic Harvesting and Rust-Readiness verified
)
COMPATIBLE_CORE_VERSIONS = ["3.0.0", "2.2.0", "2.1.0", "2.0.0"]


def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase
