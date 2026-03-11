#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/CoreExpansionAgent.description.md

# CoreExpansionAgent

**File**: `src\classes\specialized\CoreExpansionAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 80  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for CoreExpansionAgent.

## Classes (1)

### `CoreExpansionAgent`

**Inherits from**: BaseAgent

Agent responsible for autonomous environment expansion.
Detects missing libraries and installs them into the active Python environment.

**Methods** (3):
- `__init__(self, file_path)`
- `install_missing_dependency(self, package_name)`
- `audit_environment(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `pkg_resources`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/CoreExpansionAgent.improvements.md

# Improvements for CoreExpansionAgent

**File**: `src\classes\specialized\CoreExpansionAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoreExpansionAgent_test.py` with pytest tests

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

from __future__ import annotations

import logging
import subprocess
import sys

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

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
from src.core.base.version import VERSION

__version__ = VERSION


class CoreExpansionAgent(BaseAgent):
    """Agent responsible for autonomous environment expansion.
    Detects missing libraries and installs them into the active Python environment.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Core Expansion Agent. "
            "Your purpose is to ensure the swarm has the necessary tools and libraries. "
            "When a task fails due to missing dependencies, you are responsible for "
            "identifying the required packages and managing their installation."
        )

    @as_tool
    def install_missing_dependency(self, package_name: str) -> str:
        """Attempts to install a missing Python package using pip.
        """
        logging.info(
            f"CoreExpansionAgent: Attempting to install package: {package_name}"
        )

        try:
            # Use subprocess to run pip
            cmd_str = f"{sys.executable} -m pip install {package_name}"
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                check=True,
            )
            logging.info(f"CoreExpansionAgent: Successfully installed {package_name}")

            # Phase 108: Record intelligence for future dependency graph learning
            self._record(
                cmd_str, f"Success\n{result.stdout}", provider="Shell", model="pip"
            )

            return f"Success: {package_name} installed.\nStdout: {result.stdout}"
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr or str(e)
            logging.error(
                f"CoreExpansionAgent: Failed to install {package_name}. Error: {err_msg}"
            )

            # Phase 108: Record failure as a lesson
            self._record(
                f"pip install {package_name}",
                f"Failed: {err_msg}",
                provider="Shell",
                model="pip",
            )

            return f"Error: Failed to install {package_name}. Details: {err_msg}"

    @as_tool
    def audit_environment(self) -> list[str]:
        """Lists currently installed packages in the environment.
        """
        import pkg_resources

        installed_packages = [
            f"{d.project_name}=={d.version}" for d in pkg_resources.working_set
        ]
        return installed_packages
