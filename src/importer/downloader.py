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
"""Repository download helpers for PyAgent importer."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _git_binary() -> str:
    """Return the path to git, or raise if not available."""
    git = shutil.which("git")
    if not git:
        raise FileNotFoundError("git executable not found on PATH")
    return git


def clone_repo(repo_url: str, dest: Path, *, depth: int | None = 1) -> int:
    """Clone *repo_url* into *dest* using ``git clone``.

    Parameters
    ----------
    repo_url:
        The HTTPS or SSH URL of the repository.
    dest:
        Local destination path. Created if it does not exist.
    depth:
        Shallow clone depth. Pass ``None`` for a full clone.

    Returns
    -------
    int
        The git process exit code (0 == success).
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    git = _git_binary()
    cmd = [git, "clone"]
    if depth is not None:
        cmd += ["--depth", str(depth)]
    cmd += [repo_url, str(dest)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode


def download_repo(repo: str, dest: Path) -> None:
    """Compatibility shim — creates a placeholder directory for the given repo.

    For production use, prefer :func:`clone_repo` which performs a real git clone.
    """
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    readme = dest / "README.md"
    if not readme.exists():
        readme.write_text(f"# {repo}\n\nPlaceholder created by PyAgent importer.\n")
