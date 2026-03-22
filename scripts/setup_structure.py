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
"""Create the canonical PyAgent project skeleton.

This script creates the directory structure and placeholder files required
by PyAgent's TDD tests and CI pipeline. Re-running it on an existing
workspace is safe (idempotent).

Usage:
    python scripts/setup_structure.py [--root PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import sys


#: Directories that must exist for PyAgent to function correctly.
CORE_DIRECTORIES = [
    "project",
    "project/scripts",
    "project/docs",
    "project/tests/unit",
    "project/tests/integration",
    "project/tests/e2e",
    "project/src/logic/agents",
    "project/src/core/base",
    "project/src/utils",
    "project/config",
    "project/release",
    "project/scripts-old",
    "project/temp_output",
    "src/tools",
    "src/tools/plugins",
    "docs",
]

#: Empty placeholder files required in project/
PLACEHOLDER_FILES = [
    "project/llms-architecture.txt",
    "project/llms-improvements.txt",
    "project/PyAgent.md",
    "project/todolist.md",
]

#: Config scaffold files created under project/config/
CONFIG_FILES = [
    "project/config/pyproject.toml",
    "project/config/.gitignore",
    "project/config/environment.yaml",
]


def create_core_structure(root: str, dry_run: bool = False) -> None:
    """Create (or verify) the canonical directory structure under *root*.

    Parameters
    ----------
    root:
        Absolute or relative path to the workspace root.
    dry_run:
        When True, print what would be created without touching the filesystem.
    """
    created_dirs: list[str] = []
    created_files: list[str] = []

    for p in CORE_DIRECTORIES:
        full = os.path.join(root, p)
        if not os.path.isdir(full):
            if not dry_run:
                os.makedirs(full, exist_ok=True)
            created_dirs.append(full)

    # Dev-tools README
    tools_readme = os.path.join(root, "src", "tools", "README.md")
    if not os.path.exists(tools_readme):
        if not dry_run:
            with open(tools_readme, "a", encoding="utf-8"):
                pass
        created_files.append(tools_readme)

    for rel in PLACEHOLDER_FILES:
        full = os.path.join(root, rel)
        if not os.path.exists(full):
            if not dry_run:
                with open(full, "a", encoding="utf-8"):
                    pass
            created_files.append(full)

    for rel in CONFIG_FILES:
        full = os.path.join(root, rel)
        if not os.path.exists(full):
            if not dry_run:
                with open(full, "a", encoding="utf-8"):
                    pass
            created_files.append(full)

    if dry_run:
        for d in created_dirs:
            print(f"[dry-run] mkdir {d}")
        for f in created_files:
            print(f"[dry-run] touch {f}")
    else:
        for d in created_dirs:
            print(f"created dir  : {d}")
        for f in created_files:
            print(f"created file : {f}")
        if not created_dirs and not created_files:
            print("workspace already up-to-date")


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for setup_structure."""
    parser = argparse.ArgumentParser(
        prog="setup_structure",
        description="Create the canonical PyAgent directory layout.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Workspace root to create structure under (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without modifying the filesystem",
    )

    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    create_core_structure(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

