#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/agent/AgentGitHandler.description.md

# AgentGitHandler

**File**: `src\classes\agent\AgentGitHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AgentGitHandler.

## Classes (1)

### `AgentGitHandler`

Handles git operations for the Agent.

**Methods** (4):
- `__init__(self, repo_root, no_git, recorder)`
- `_record(self, action, result, meta)`
- `commit_changes(self, message, files)`
- `create_branch(self, branch_name)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/AgentGitHandler.improvements.md

# Improvements for AgentGitHandler

**File**: `src\classes\agent\AgentGitHandler.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 84 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentGitHandler_test.py` with pytest tests

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
import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Any, Dict

__version__ = VERSION


class AgentGitHandler:
    """Handles git operations for the Agent."""

    def __init__(
        self, repo_root: Path, no_git: bool = False, recorder: Any = None
    ) -> None:
        self.repo_root: Path = repo_root
        self.no_git: bool = no_git
        self.recorder: Any = recorder

    def _record(
        self, action: str, result: str, meta: dict[str, Any] | None = None
    ) -> None:
        """Internal helper to record git operations if recorder is available."""
        if self.recorder:
            self.recorder.record_interaction(
                provider="Git", model="cli", prompt=action, result=result, meta=meta
            )

    def commit_changes(self, message: str, files: list[str] | None = None) -> None:
        """Commit changes to the repository."""
        if self.no_git:
            logging.info(f"Skipping git commit: no_git=True. Message: {message}")
            return

        try:
            if files:
                for file in files:
                    subprocess.run(
                        ["git", "add", file],
                        cwd=self.repo_root,
                        check=True,
                        capture_output=True,
                    )
            else:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.repo_root,
                    check=True,
                    capture_output=True,
                )

            # Check if there are changes to commit
            status: str = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
            ).stdout.strip()
            if not status:
                logging.info("No changes to commit.")
                return

            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )
            logging.info(f"Successfully committed changes: {message}")
            self._record(f"commit: {message}", "success", {"files": files})
        except subprocess.CalledProcessError as e:
            err_msg: str = e.stderr.strip() if e.stderr else str(e)
            logging.error(f"Git commit failed: {err_msg}")
            self._record(f"commit: {message}", f"failed: {err_msg}")
        except Exception as e:
            logging.error(f"Error during git commit: {e}")
            self._record(f"commit: {message}", f"error: {str(e)}")

    def create_branch(self, branch_name: str) -> bool:
        """Create and switch to a new branch."""
        if self.no_git:
            return False
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )
            logging.info(f"Created branch: {branch_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to create branch {branch_name}: {e}")
            return False
