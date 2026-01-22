# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Git Core for PyAgent.
Standardizes branch management, commits, and status retrieval.
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
from src.core.base.common.shell_core import ShellCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class GitCore(BaseCore):
    """
    Standard implementation for Git operations.
    If rc is available, delegates to native libgit2 hooks for speed.
    """
    
    def __init__(self, repo_root: Path, no_git: bool = False):
        super().__init__()
        self.repo_root = repo_root
        self.no_git = no_git
        self.shell = ShellCore(repo_root=repo_root)

    def commit(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Commits changes to the repository."""
        if self.no_git: return False
        
        if rc and hasattr(rc, "git_commit_rust"):
            return rc.git_commit_rust(str(self.repo_root), message, files)
            
        file_args = "." if not files else " ".join(files)
        self.shell.run(f"git add {file_args}")
        self.shell.run(f"git commit -m \"{message}\"")
        return True

    def get_status(self) -> str:
        """Retrieves the current git status."""
        if self.no_git: return ""
        return self.shell.run("git status").stdout

    def branch(self, name: str) -> bool:
        """Creates or switches to a branch."""
        if self.no_git: return False
        self.shell.run(f"git checkout -b {name}")
        return True
