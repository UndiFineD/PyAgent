"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SelfHealingEngineCore.description.md

# SelfHealingEngineCore

**File**: `src\classes\orchestration\SelfHealingEngineCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 33  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SelfHealingEngineCore.

## Classes (1)

### `SelfHealingEngineCore`

Pure logic for self-healing analysis.
Decides what kind of fix is needed based on the traceback.

**Methods** (2):
- `analyze_failure(self, agent_name, tool_name, error_msg, tb)`
- `format_healing_report(self, history)`

## Dependencies

**Imports** (4):
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SelfHealingEngineCore.improvements.md

# Improvements for SelfHealingEngineCore

**File**: `src\classes\orchestration\SelfHealingEngineCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 33 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SelfHealingEngineCore_test.py` with pytest tests

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

import traceback
from typing import Dict, List, Any


class SelfHealingEngineCore:
    """
    Pure logic for self-healing analysis.
    Decides what kind of fix is needed based on the traceback.
    """

    def analyze_failure(
        self, agent_name: str, tool_name: str, error_msg: str, tb: str
    ) -> Dict[str, Any]:
        """Analyzes a failure and suggests a strategy."""
        strategy = "manual_review"

        if "SyntaxError" in tb:
            strategy = "fix_syntax"
        elif "ImportError" in tb:
            strategy = "install_dependency"
        elif "KeyError" in tb:
            strategy = "check_config"
        elif "AttributeError" in tb:
            strategy = "verify_api_compatibility"

        return {
            "agent": agent_name,
            "tool": tool_name,
            "error": error_msg,
            "strategy": strategy,
            "is_critical": "Registry" in agent_name or "Fleet" in agent_name,
        }

    def format_healing_report(self, history: List[Dict[str, Any]]) -> str:
        """Standardized reporting logic."""
        return f"Self-Healing Engine: {len(history)} failures detected and queued for repair."
