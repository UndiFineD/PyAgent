#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/SafetyAuditTrail.description.md

# SafetyAuditTrail

**File**: `src\classes\fleet\SafetyAuditTrail.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 50  
**Complexity**: 5 (moderate)

## Overview

Persistent audit log for safety violations and adversarial attempts.

## Classes (1)

### `SafetyAuditTrail`

Logs security violations for later forensic analysis and training.

**Methods** (5):
- `__init__(self, log_path)`
- `_load_log(self)`
- `log_violation(self, agent_name, task, violations, level)`
- `_save_log(self)`
- `get_summary(self)`

## Dependencies

**Imports** (4):
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/SafetyAuditTrail.improvements.md

# Improvements for SafetyAuditTrail

**File**: `src\classes\fleet\SafetyAuditTrail.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SafetyAuditTrail_test.py` with pytest tests

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

"""Persistent audit log for safety violations and adversarial attempts."""

import json
import logging
from pathlib import Path
from datetime import datetime


class SafetyAuditTrail:
    """Logs security violations for later forensic analysis and training."""

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.violations = []
        self._load_log()

    def _load_log(self) -> str:
        if self.log_path.exists():
            try:
                with open(self.log_path, "r") as f:
                    self.violations = json.load(f)
            except Exception as e:
                logging.error(f"SafetyAuditTrail: Error loading log: {e}")

    def log_violation(
        self, agent_name: str, task: str, violations: list, level: str = "HIGH"
    ) -> str:
        """Records a new safety violation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "level": level,
            "violations": violations,
            "context": task[:500],
        }
        self.violations.append(entry)
        self._save_log()
        logging.warning(f"SafetyAuditTrail: Logged {level} violation for {agent_name}.")

    def _save_log(self) -> str:
        try:
            with open(self.log_path, "w") as f:
                json.dump(self.violations, f, indent=2)
        except Exception as e:
            logging.error(f"SafetyAuditTrail: Error saving log: {e}")

    def get_summary(self) -> str:
        """Returns a human-readable summary of recently logged threats."""
        if not self.violations:
            return "No safety violations recorded."
        return f"Safety Audit: {len(self.violations)} threats recorded. Latest: {self.violations[-1]['level']} at {self.violations[-1]['timestamp']}"
