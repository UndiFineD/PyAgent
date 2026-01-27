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
Restore Except As E module.
"""

from pathlib import Path

def restore_except_as_e(root_dir):
    """
    Restore 'except Exception as e' pattern in codebase.

    Args:
        root_dir: The root directory to search in.
    """
    target = "except Exception:  # pylint: disable=broad-exception-caught"
    replacement = "except Exception as e:  # pylint: disable=broad-exception-caught"
    root = Path(root_dir)
    for p in root.rglob("*.py"):
        try:
            content = p.read_text(encoding="utf-8")
            if target in content:
                new_content = content.replace(target, replacement)
                p.write_text(new_content, encoding="utf-8")
                print(f"Restored except as e in {p}")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            print(f"Error restoring {p}: {e}")

if __name__ == "__main__":
    # Robustly find the repository root
    current_path = Path(__file__).resolve()
    project_root = current_path
    while project_root.name != 'src' and project_root.parent != project_root:
        project_root = project_root.parent
    if project_root.name == 'src':
        project_root = project_root.parent

    restore_except_as_e(project_root / "src")
    restore_except_as_e(project_root / "tests")
