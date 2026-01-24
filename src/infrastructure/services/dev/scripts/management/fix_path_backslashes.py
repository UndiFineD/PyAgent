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
Utility to fix backslash escaping issues in paths (e.g., c:\" -> c:\\").
Ported from temp/fix_backslashes.py.
"""

import argparse
import os
from pathlib import Path


def fix_path_backslashes(target_dirs: list[str]):
    """Recursively fixes malformed path strings in Python files."""
    workspace_root = Path(__file__).resolve().parents[5]

    for folder_rel in target_dirs:
        folder = workspace_root / folder_rel
        if not folder.exists():
            print(f"Skipping non-existent folder: {folder_rel}")
            continue

        print(f"Checking {folder_rel} for path backslash errors...")
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".py"):
                    path = Path(root) / file
                    try:
                        content = path.read_text(encoding="utf-8")

                        # Fix backslash escaping quote issue: c:\" -> c:\\"
                        new_content = content.replace('c:\\"', 'c:\\\\"').replace('C:\\"', 'C:\\\\"')

                        if new_content != content:
                            path.write_text(new_content, encoding="utf-8")
                            print(f"Fixed backslashes: {path.relative_to(workspace_root)}")
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix malformed path backslashes.")
    parser.add_argument("--dirs", nargs="+", default=["src"], help="Directories to scan.")

    args = parser.parse_args()
    fix_path_backslashes(args.dirs)
