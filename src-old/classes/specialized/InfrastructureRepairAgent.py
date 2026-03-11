#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/InfrastructureRepairAgent.description.md

# InfrastructureRepairAgent

**File**: `src\classes\specialized\InfrastructureRepairAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 63  
**Complexity**: 4 (simple)

## Overview

Agent for automated infrastructure and environment repair.
Detects and fixes environment issues like missing dependencies or broken paths.

## Classes (1)

### `InfrastructureRepairAgent`

**Inherits from**: BaseAgent

Monitors and repairs the agent's execution environment.

**Methods** (4):
- `__init__(self, path)`
- `audit_environment(self)`
- `repair_issue(self, issue)`
- `auto_repair(self)`

## Dependencies

**Imports** (6):
- `logging`
- `pandas`
- `src.classes.base_agent.BaseAgent`
- `subprocess`
- `sys`
- `yaml`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/InfrastructureRepairAgent.improvements.md

# Improvements for InfrastructureRepairAgent

**File**: `src\classes\specialized\InfrastructureRepairAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 63 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `InfrastructureRepairAgent_test.py` with pytest tests

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

"""Agent for automated infrastructure and environment repair.
Detects and fixes environment issues like missing dependencies or broken paths.
"""

import logging
import subprocess
import sys

from src.classes.base_agent import BaseAgent


class InfrastructureRepairAgent(BaseAgent):
    """Monitors and repairs the agent's execution environment."""

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.name = "InfrastructureRepair"

    def audit_environment(self) -> dict:
        """Checks for common environment issues."""
        issues = []

        # Check for common packages
        try:
            import pandas
        except ImportError:
            issues.append({"type": "missing_package", "package": "pandas"})

        try:
            import yaml
        except ImportError:
            issues.append({"type": "missing_package", "package": "pyyaml"})

        return {"status": "clean" if not issues else "degraded", "issues": issues}

    def repair_issue(self, issue: dict) -> str:
        """Attempts to fix a detected environment issue."""
        if issue["type"] == "missing_package":
            package = issue["package"]
            logging.info(f"Environment: Attempting to install {package}...")
            cmd_str = f"pip install {package}"
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                self._record(cmd_str, "Success", provider="Shell", model="pip")
                return f"Successfully installed {package}."
            except Exception as e:
                self._record(
                    cmd_str, f"Failed: {str(e)}", provider="Shell", model="pip"
                )
                return f"Failed to install {package}: {e}"

        return "Unknown issue type."

    def auto_repair(self) -> str:
        """Runs audit and attempts to fix all issues found."""
        report = self.audit_environment()
        if report["status"] == "clean":
            return "Environment is healthy."

        results = []
        for issue in report["issues"]:
            res = self.repair_issue(issue)
            results.append(res)

        return "\n".join(results)
