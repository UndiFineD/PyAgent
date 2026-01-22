<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Git Core for PyAgent.
Standardizes branch management, commits, and status retrieval.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

from pathlib import Path
from typing import List, Optional

from .base_core import BaseCore
from .shell_core import ShellCore
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
from src.core.base.common.shell_core import ShellCore
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class GitCore(BaseCore):
    """
    Standard implementation for Git operations.
    If rc is available, delegates to native libgit2 hooks for speed.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, repo_root: Path, no_git: bool = False) -> None:
=======
    
    def __init__(self, repo_root: Path, no_git: bool = False):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self, repo_root: Path, no_git: bool = False):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self.repo_root = repo_root
        self.no_git = no_git
        self.shell = ShellCore(repo_root=repo_root)

    def commit(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Commits changes to the repository."""
<<<<<<< HEAD
<<<<<<< HEAD
        if self.no_git:
            return False

        if rc and hasattr(rc, "git_commit_rust"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.git_commit_rust(str(self.repo_root), message, files)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        if files:
            self.shell.execute(["git", "add"] + files)
        else:
            self.shell.execute(["git", "add", "."])

        self.shell.execute(["git", "commit", "-m", message])
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if self.no_git: return False
        
        if rc and hasattr(rc, "git_commit_rust"):
            return rc.git_commit_rust(str(self.repo_root), message, files)
            
        file_args = "." if not files else " ".join(files)
        self.shell.run(f"git add {file_args}")
        self.shell.run(f"git commit -m \"{message}\"")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return True

    def get_status(self) -> str:
        """Retrieves the current git status."""
<<<<<<< HEAD
<<<<<<< HEAD
        if self.no_git:
            return ""
        return self.shell.execute(["git", "status"]).stdout

    def branch(self, name: str) -> bool:
        """Creates or switches to a branch."""
        if self.no_git:
            return False
        self.shell.execute(["git", "checkout", "-b", name])
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if self.no_git: return ""
        return self.shell.run("git status").stdout

    def branch(self, name: str) -> bool:
        """Creates or switches to a branch."""
        if self.no_git: return False
        self.shell.run(f"git checkout -b {name}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return True
