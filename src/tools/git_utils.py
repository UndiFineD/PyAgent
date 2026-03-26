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

"""Git and GitHub helper utilities.

Provides programmatic wrappers for common git operations used by PyAgent
agents during the development workflow.  All subprocess calls use explicit
argument lists — never shell=True.
"""

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run_git(
    args: Iterable[str], capture_output: bool = False, cwd: str | None = None
) -> subprocess.CompletedProcess[str]:
    """Run a git command.  Never uses shell=True."""
    return subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        check=False,
        capture_output=capture_output,
        text=True,
        cwd=cwd,
    )


def _get_merge_base(base: str) -> str | None:
    """Return the merge-base commit hash between HEAD and *base*, or None."""
    proc = _run_git(["merge-base", "HEAD", base], capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _current_branch() -> str:
    """Return the current branch name."""
    proc = _run_git(["branch", "--show-current"], capture_output=True)
    return proc.stdout.strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_feature_branch(name: str, base: str = "main") -> bool:
    """Create and checkout a new feature branch from *base*.

    Parameters
    ----------
    name:
        Branch name to create (e.g. ``"feat/my-feature"``).
    base:
        Base branch to branch from (default ``"main"``).

    Returns
    -------
    bool
        True on success, False if git returned a non-zero exit code.

    """
    # Fetch latest base first (ignore errors — may be offline)
    _run_git(["fetch", "origin", base])
    proc = _run_git(["checkout", "-b", name, f"origin/{base}"])
    return proc.returncode == 0


def changed_files(base: str = "main") -> list[str]:
    """Return a list of files changed relative to *base* branch."""
    merge_base = _get_merge_base(base)
    if not merge_base:
        return []
    proc = _run_git(["diff", "--name-only", merge_base, "HEAD"], capture_output=True)
    if not proc.stdout.strip():
        return []
    return proc.stdout.strip().splitlines()


def update_changelog(entry: str, changelog_path: str = "CHANGELOG.md") -> None:
    """Prepend a dated entry to *changelog_path*.

    Creates the file if it does not exist.

    Parameters
    ----------
    entry:
        Changelog text for the new entry.
    changelog_path:
        Path to the changelog file.

    """
    p = Path(changelog_path)
    today = datetime.date.today().isoformat()
    new_entry = f"## {today}\n\n{entry.strip()}\n\n"

    if p.exists():
        existing = p.read_text(encoding="utf-8")
        p.write_text(new_entry + existing, encoding="utf-8")
    else:
        p.write_text(f"# Changelog\n\n{new_entry}", encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(args: list[str] | None = None) -> int:
    """CLI entrypoint for git helper utilities."""
    parser = argparse.ArgumentParser(prog="git_utils", description="Git workflow helpers.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Run `git status`")

    log_p = sub.add_parser("log", help="Run `git log`")
    log_p.add_argument("-n", "--number", type=int, default=5)

    changed_p = sub.add_parser("changed", help="Show changed files relative to a base branch")
    changed_p.add_argument("--base", default="main")

    branch_p = sub.add_parser("branch", help="Create a feature branch")
    branch_p.add_argument("name", help="Branch name")
    branch_p.add_argument("--base", default="main")

    cl_p = sub.add_parser("changelog", help="Prepend an entry to CHANGELOG.md")
    cl_p.add_argument("entry", help="Changelog entry text")
    cl_p.add_argument("--file", default="CHANGELOG.md")

    parsed = parser.parse_args(args=args)

    if parsed.command == "status":
        return _run_git(["status"]).returncode

    if parsed.command == "log":
        return _run_git(["log", f"-n{parsed.number}"]).returncode

    if parsed.command == "changed":
        files = changed_files(parsed.base)
        if files:
            print("\n".join(files))
        return 0

    if parsed.command == "branch":
        ok = create_feature_branch(parsed.name, base=parsed.base)
        if ok:
            print(f"Created and switched to branch: {parsed.name}")
        else:
            print(f"Failed to create branch: {parsed.name}", file=sys.stderr)
        return 0 if ok else 1

    if parsed.command == "changelog":
        update_changelog(parsed.entry, parsed.file)
        print(f"Updated {parsed.file}")
        return 0

    parser.print_help()
    return 1


# Register tool for CLI discovery
register_tool("git-utils", main, "Git workflow helpers (branch, changelog, changed files)")
register_tool("9git", main, "Git helper for the @9git agent workflow")


if __name__ == "__main__":
    sys.exit(main())
