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


def _run_git(args: Iterable[str]) -> int:
    proc = subprocess.run(["git", *args], check=False)
    return proc.returncode


def main(args: list[str] | None = None) -> int:
    """CLI entrypoint for git helper utilities."""
    parser = argparse.ArgumentParser(prog="git_utils")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Run `git status`")
    log = sub.add_parser("log", help="Run `git log`")
    log.add_argument("-n", "--number", type=int, default=5, help="Number of commits")

    parsed = parser.parse_args(args=args)

    if parsed.command == "status":
        return _run_git(["status"])
    if parsed.command == "log":
        return _run_git(["log", f"-n{parsed.number}"])

    parser.print_help()
    return 1


# Register tool for CLI discovery
register_tool("git-utils", main, "Git wrapper utilities")

# Alias for the 9git agent workflow
register_tool("9git", main, "Git helper for the @9git agent")


if __name__ == "__main__":
    sys.exit(main())
