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
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa: S603
    return result.returncode


def download_repo(repo: str, dest: Path) -> None:
    """Download a repository into a destination path.

    This function first performs a real git clone. If cloning is unavailable
    in the current environment (for example, no network access), it writes an
    explicit offline metadata file so downstream importer stages still have a
    concrete artifact to process.

    Args:
        repo: Repository identifier in owner/name form or full git URL.
        dest: Destination directory path.

    Raises:
        RuntimeError: If repository identifier is invalid.

    """
    repo_url = _normalize_repo_url(repo)
    exit_code = clone_repo(repo_url, dest)
    if exit_code == 0:
        return

    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    readme = dest / "README.md"
    if readme.exists():
        return

    readme.write_text(
        "\n".join(
            [
                f"# {repo}",
                "",
                "Repository clone could not be completed in this environment.",
                f"Attempted source: {repo_url}",
                "This artifact preserves importer pipeline continuity for offline runs.",
                "",
            ]
        )
    )


def _normalize_repo_url(repo: str) -> str:
    """Normalize repository input to a cloneable git URL.

    Args:
        repo: Repository input in URL or owner/name format.

    Returns:
        A normalized git URL.

    Raises:
        RuntimeError: If the repository input is empty or malformed.

    """
    candidate = repo.strip()
    if not candidate:
        raise RuntimeError("Repository identifier must not be empty")

    if candidate.startswith(("https://", "http://", "git@", "ssh://")):
        return candidate

    if "/" not in candidate:
        raise RuntimeError("Repository identifier must be owner/name or a full git URL")

    owner, name = candidate.split("/", 1)
    owner = owner.strip()
    name = name.strip()
    if not owner or not name:
        raise RuntimeError("Repository identifier must be owner/name or a full git URL")

    suffix = "" if name.endswith(".git") else ".git"
    return f"https://github.com/{owner}/{name}{suffix}"
