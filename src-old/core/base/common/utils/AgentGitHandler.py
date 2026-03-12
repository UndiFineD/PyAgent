#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/core/base/common/utils/AgentGitHandler.description.md

# AgentGitHandler

**File**: `src\core\base\common\utils\AgentGitHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for AgentGitHandler.

## Classes (1)

### `AgentGitHandler`

Handles git operations for the Agent.

**Methods** (3):
- `__init__(self, repo_root, no_git)`
- `commit_changes(self, message, files)`
- `create_branch(self, branch_name)`

## Dependencies

**Imports** (5):
- `logging`
- `pathlib.Path`
- `subprocess`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/common/utils/AgentGitHandler.improvements.md

# Improvements for AgentGitHandler

**File**: `src\core\base\common\utils\AgentGitHandler.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentGitHandler_test.py` with pytest tests

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

import subprocess
import logging
from pathlib import Path
from typing import List, Optional


class AgentGitHandler:
    """Handles git operations for the Agent."""

    def __init__(self, repo_root: Path, no_git: bool = False) -> None:
        self.repo_root = repo_root
        self.no_git = no_git

    def commit_changes(self, message: str, files: Optional[List[str]] = None):
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
            status = subprocess.run(
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
        except subprocess.CalledProcessError as e:
            logging.error(f"Git commit failed: {e.stderr.strip() if e.stderr else e}")
        except Exception as e:
            logging.error(f"Error during git commit: {e}")

    def create_branch(self, branch_name: str):
        """Create and switch to a new branch."""
        if self.no_git:
            return
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )
            logging.info(f"Created branch: {branch_name}")
        except Exception as e:
            logging.error(f"Failed to create branch {branch_name}: {e}")
