#!/usr/bin/env python3
"""Git and GitHub helper utilities."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import Iterable

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def _run_git(args: Iterable[str], capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], check=False, capture_output=capture_output, text=True)


def _get_merge_base(base: str) -> str | None:
    proc = _run_git(["merge-base", "HEAD", base], capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def main(args: list[str] | None = None) -> int:
    """CLI entrypoint for git helper utilities."""
    parser = argparse.ArgumentParser(prog="git_utils")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Run `git status`")
    log = sub.add_parser("log", help="Run `git log`")
    log.add_argument("-n", "--number", type=int, default=5, help="Number of commits")

    changed = sub.add_parser("changed", help="Show changed files relative to main branch")
    changed.add_argument("--base", default="main", help="Base branch to compare against")

    parsed = parser.parse_args(args=args)

    if parsed.command == "status":
        return _run_git(["status"]).returncode
    if parsed.command == "log":
        return _run_git(["log", f"-n{parsed.number}"]).returncode
    if parsed.command == "changed":
        base = parsed.base
        merge_base = _get_merge_base(base)
        if not merge_base:
            print(f"Unable to determine merge base against {base}", file=sys.stderr)
            return 1

        proc = _run_git(["diff", "--name-only", merge_base, "HEAD"], capture_output=True)
        if proc.stdout:
            print(proc.stdout.strip())
        return proc.returncode

    parser.print_help()
    return 1


# Register tool for CLI discovery
register_tool("git-utils", main, "Git wrapper utilities")

# Alias for the 9git agent workflow
register_tool("9git", main, "Git helper for the @9git agent")


if __name__ == "__main__":
    sys.exit(main())
