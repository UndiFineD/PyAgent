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
Deduplicate Excepts module.
"""

from pathlib import Path


def deduplicate_excepts(root_dir):
    """
    Scans the directory to deduplicate except blocks handling generic exceptions.

    Args:
        root_dir: The root directory to scan recursively.
    """
    target = "except Exception as e:  # pylint: disable=broad-exception-caught"
    root = Path(root_dir)
    for p in root.rglob("*.py"):
        try:
            content = p.read_text(encoding="utf-8")
            if target not in content:
                continue

            lines = content.splitlines()
            new_lines = []
            modified = False
            last_line = ""
            for line in lines:
                if target in line and target in last_line:
                    # Duplicate!
                    modified = True
                    continue
                new_lines.append(line)
                last_line = line

            if modified:
                p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                print(f"Deduplicated excepts in {p}")
        except (IOError, OSError, UnicodeDecodeError) as e:
            print(f"Error deduplicating {p}: {e}")


if __name__ == "__main__":
    # Robustly find the repository root
    current_path = Path(__file__).resolve()
    project_root = current_path
    while project_root.name != 'src' and project_root.parent != project_root:
        project_root = project_root.parent
    if project_root.name == 'src':
        project_root = project_root.parent

    deduplicate_excepts(project_root / "src")
    deduplicate_excepts(project_root / "tests")
