#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/TestAgent.description.md

# TestAgent

**File**: `src\classes\coder\TestAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 64  
**Complexity**: 4 (simple)

## Overview

Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.

## Classes (1)

### `TestAgent`

**Inherits from**: BaseAgent

Executes unit and integration tests and analyzes failures.

**Methods** (4):
- `__init__(self, file_path)`
- `run_tests(self, path)`
- `run_file_tests(self, file_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/TestAgent.improvements.md

# Improvements for TestAgent

**File**: `src\classes\coder\TestAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TestAgent_test.py` with pytest tests

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

"""Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.
"""

import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class TestAgent(BaseAgent):
    """Executes unit and integration tests and analyzes failures."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Test Agent. "
            "Your role is to ensure the functional correctness of the codebase. "
            "Execute pytest suites, capture failures, and explain them to the developers. "
            "Always suggest a potential cause for every test failure."
        )

    @as_tool
    def run_tests(self, path: str = "tests") -> str:
        """Executes pytest on the specified directory."""
        logging.info(f"TestAgent running tests in: {path}")
        try:
            import sys

            # Converted to list-based execution to prevent shell injection
            cmd = [sys.executable, "-m", "pytest", path, "--tb=short", "--maxfail=5"]
            result = subprocess.run(cmd, shell=False, capture_output=True, text=True)

            # Phase 108: Record test execution patterns
            self._record(
                f"pytest {path}",
                f"RC={result.returncode}\n{result.stdout[-1000:]}",
                provider="Shell",
                model="pytest",
            )

            report = ["## 🧪 Test Execution Report\n"]
            if result.returncode == 0:
                report.append("✅ **Status**: All tests passed.")
                report.append(
                    f"```text\n{result.stdout.splitlines()[-1]}\n```"
                )  # Last line summary
            else:
                report.append(f"❌ **Status**: {result.returncode} tests FAILED.\n")
                report.append("### Failure Details")
                report.append(f"```text\n{result.stdout}\n```")

            return "\n".join(report)
        except Exception as e:
            return f"Error running tests: {e}"

    @as_tool
    def run_file_tests(self, file_path: str) -> str:
        """Runs tests for a single file."""
        return self.run_tests(file_path)

    def improve_content(self, prompt: str) -> str:
        """Runs tests based on user prompt."""
        return self.run_tests()
