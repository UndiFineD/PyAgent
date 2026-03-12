#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/LintingAgent.description.md

# LintingAgent

**File**: `src\classes\coder\LintingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in code quality, linting, and style enforcement.

## Classes (1)

### `LintingAgent`

**Inherits from**: BaseAgent

Ensures code adheres to quality standards by running linters.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `run_flake8(self, target_path)`
- `run_mypy(self, target_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/LintingAgent.improvements.md

# Improvements for LintingAgent

**File**: `src\classes\coder\LintingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LintingAgent_test.py` with pytest tests

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

"""Agent specializing in code quality, linting, and style enforcement."""

import subprocess

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function


class LintingAgent(BaseAgent):
    """Ensures code adheres to quality standards by running linters."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Linting Agent. "
            "Your role is to ensure the codebase is clean, readable, and free of syntax errors. "
            "You use tools like flake8 and mypy to catch issues before they reach production."
        )

    def _get_default_content(self) -> str:
        return "# Code Quality Report\n\n## Summary\nAll clear.\n"

    def run_flake8(self, target_path: str) -> str:
        """Runs flake8 on the specified path."""
        try:
            # We use --max-line-length=120 and ignore some common ones
            result = subprocess.run(
                ["flake8", "--max-line-length=120", "--ignore=E203,W503", target_path],
                capture_output=True,
                text=True,
            )
            # Phase 108: Record linting result
            self._record(
                f"flake8 {target_path}",
                f"RC={result.returncode}\n{result.stdout[:500]}",
                provider="Shell",
                model="flake8",
            )

            if not result.stdout:
                return "✅ No linting issues found by flake8."
            return f"### Flake8 Issues\n```plaintext\n{result.stdout}\n```"
        except FileNotFoundError:
            return "❌ flake8 not installed in the current environment."
        except Exception as e:
            return f"❌ Error running flake8: {e}"

    def run_mypy(self, target_path: str) -> str:
        """Runs mypy type checking."""
        try:
            result = subprocess.run(
                ["mypy", "--ignore-missing-imports", target_path],
                capture_output=True,
                text=True,
            )
            if "Success: no issues found" in result.stdout:
                return "✅ No type issues found by mypy."
            return f"### Mypy Issues\n```plaintext\n{result.stdout}\n```"
        except FileNotFoundError:
            return "❌ mypy not installed in the current environment."
        except Exception as e:
            return f"❌ Error running mypy: {e}"

    def improve_content(self, prompt: str) -> str:
        """Perform a quality audit on a file or directory."""
        # prompt is expected to be a path
        path = prompt if prompt else "."
        flake8_res = self.run_flake8(path)
        mypy_res = self.run_mypy(path)

        return f"## Quality Audit for: {path}\n\n" f"{flake8_res}\n\n" f"{mypy_res}"


if __name__ == "__main__":
    main = create_main_function(LintingAgent, "Linting Agent", "Path to audit")
    main()
