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

"""
Unified workspace and path management core.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified workspace and path management core."""

import os
import logging
from pathlib import Path
from typing import Set, Dict, Optional, Union, List
import time
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
class WorkspaceCore:
    """
    Centralized handler for workspace-wide path logic and file ignore rules.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    _instance: Optional["WorkspaceCore"] = None
    _ignore_cache: Dict[str, Set[str]] = {}
    _ignore_cache_time: Dict[str, float] = {}
    _initialized: bool = False

    def __new__(cls, root_dir: Optional[Union[str, Path]] = None) -> "WorkspaceCore":
        """Singleton pattern for workspace core."""
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    _instance: Optional['WorkspaceCore'] = None
    _ignore_cache: Dict[str, Set[str]] = {}
    _ignore_cache_time: Dict[str, float] = {}

    def __new__(cls, root_dir: Optional[Union[str, Path]] = None):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if cls._instance is None:
            cls._instance = super(WorkspaceCore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, root_dir: Optional[Union[str, Path]] = None) -> None:
        """Initialize the workspace root and logger."""
        if self._initialized:
            return

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def __init__(self, root_dir: Optional[Union[str, Path]] = None):
        if self._initialized:
            return
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if root_dir:
            self.root_dir = Path(root_dir)
        else:
            # Simple fallback root detection to avoid recursion with ConfigManager
            curr = Path.cwd()
            self.root_dir = curr
            for parent in [curr] + list(curr.parents):
<<<<<<< HEAD
<<<<<<< HEAD
                if (
                    (parent / ".git").exists()
                    or (parent / "pyproject.toml").exists()
                    or (parent / "requirements.txt").exists()
                ):
                    self.root_dir = parent
                    break

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                if (parent / ".git").exists() or (parent / "pyproject.toml").exists() or (parent / "requirements.txt").exists():
                    self.root_dir = parent
                    break
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.logger = logging.getLogger("pyagent.workspace")
        self._initialized = True

    def get_path(self, *parts: str) -> Path:
        """Resolve a path relative to the workspace root."""
        return self.root_dir.joinpath(*parts)

    def get_relative_path(self, path: Union[str, Path]) -> str:
        """Standardize a path to a string relative to the workspace root."""
        p = Path(path)
        try:
            if p.is_absolute():
                return str(p.relative_to(self.root_dir)).replace("\\", "/")
            return str(p).replace("\\", "/")
        except ValueError:
            return str(p).replace("\\", "/")

    def is_ignored(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file path matches any patterns in .codeignore.
        """
        path = Path(file_path)
        if path.is_absolute():
            try:
                path = path.relative_to(self.root_dir)
            except ValueError:
                # Not in workspace, can't be ignored by workspace rules
                return False
<<<<<<< HEAD
<<<<<<< HEAD

=======
                
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        patterns = self.get_ignore_patterns()
        # Basic glob matching for simplicity in this core
        # In a real scenario, we might use a library like 'pathspec'
        path_str = str(path).replace("\\", "/")
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        for pattern in patterns:
            if pattern.endswith("/") and path_str.startswith(pattern.rstrip("/")):
                return True
            if pattern in path_str:
                return True
        return False

    def get_ignore_patterns(self) -> Set[str]:
        """Load and parse ignore patterns from .codeignore with caching."""
        ignore_path = self.root_dir / ".codeignore"
        cache_key = str(ignore_path)

        if not ignore_path.exists():
            return set()

        if rc and hasattr(rc, "parse_codeignore_rust"): # pylint: disable=no-member
            try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                patterns = rc.parse_codeignore_rust(str(ignore_path))  # pylint: disable=no-member
                return set(patterns)
            except Exception as err:  # pylint: disable=broad-exception-caught, unused-variable
                self.logger.warning("Rust ignore parsing failed: %s", err)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                patterns = rc.parse_codeignore_rust(str(ignore_path))
=======
                patterns = rc.parse_codeignore_rust(str(ignore_path)) # type: ignore
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
                return set(patterns)
            except Exception as e: # pylint: disable=broad-exception-caught
                self.logger.warning(f"Rust ignore parsing failed: {e}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        try:
            mtime = ignore_path.stat().st_mtime
            if cache_key in self._ignore_cache and self._ignore_cache_time.get(cache_key) == mtime:
                return self._ignore_cache[cache_key]

            content = ignore_path.read_text(encoding="utf-8")
            patterns = {
<<<<<<< HEAD
<<<<<<< HEAD
                line.strip() for line in content.split("\n") if line.strip() and not line.strip().startswith("#")
            }

            self._ignore_cache[cache_key] = patterns
            self._ignore_cache_time[cache_key] = mtime
            return patterns

        except Exception as err:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.warning("Failed to read .codeignore: %s", err)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                line.strip()
                for line in content.split("\n")
                if line.strip() and not line.strip().startswith("#")
            }
            
            self._ignore_cache[cache_key] = patterns
            self._ignore_cache_time[cache_key] = mtime
            return patterns
            
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.warning(f"Failed to read .codeignore: {e}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return set()

    def list_files(self, relative_path: str = ".", pattern: str = "*") -> List[Path]:
        """List files in a directory, respecting ignore rules."""
        target_dir = self.root_dir / relative_path
        if not target_dir.exists():
            return []
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        files = []
        for file in target_dir.rglob(pattern):
            if not self.is_ignored(file):
                files.append(file)
        return files
