#!/usr/bin/env python3
"""Enforce git branch naming as part of the pre-commit workflow.

This script is intended to be run as a pre-commit hook. It verifies that the
current git branch follows the expected naming convention for project work.

Rules:
- Allowed branches: `main`, `master`, `dev`, `develop`.
- Project branches MUST match `prj###-<slug>` (e.g. `prj001-core-system`).
"""

from __future__ import annotations

import re
import subprocess
import sys


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    branch = get_current_branch()

    allowed = {"main", "master", "dev", "develop"}
    prj_pattern = re.compile(r"^prj\d{3}-[a-z0-9-]+$")

    if branch in allowed or prj_pattern.match(branch):
        return 0

    print(
        "\nERROR: Branch name does not follow the expected workflow naming convention.\n"
        "Please create and use a branch matching `prj###-<slug>` (e.g. `prj001-core-system`)\n"
        "or use one of: main, master, dev, develop.\n"
        f"Current branch: {branch}\n"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
