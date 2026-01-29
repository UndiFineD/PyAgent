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
Recover Indentation module.
"""

#!/usr/bin/env python3
import re
from pathlib import Path

def fix_broken_indentation(root_dir):
    """
    Fix indentation broken by previous refactoring.
    """
    # pattern = re.compile(r"(except Exception as e:  # pylint: disable=broad-exception-caught)\n(\s*)(\S)")
    # The previous fix likely deleted the indentation of the next line.
    # Wait, the previous fix replaced `except Exception:\s*`
    # If the file was:
    # 1:         try:
    # 2:             dostuff()
    # 3:         except Exception:
    # 4:             pass
    #
    # \s* matched "\n            "
    # Replacing it with "except ...\n" resulted in:
    # 3:         except Exception as e: ...
    # 4: pass

    # We need to find `except Exception as e: ...\n` and indent the NEXT line
    # based on the indentation of the `except` line plus 4 spaces.

    root = Path(root_dir)
    for p in root.rglob("*.py"):
        try:
            content = p.read_text(encoding="utf-8")
            if "pylint: disable=broad-exception-caught" not in content:
                continue

            lines = content.splitlines()
            new_lines = []
            modified = False
            i = 0
            while i < len(lines):
                line = lines[i]
                if "pylint: disable=broad-exception-caught" in line and "except" in line:
                    new_lines.append(line)
                    # The next line might be missing indentation
                    if i + 1 < len(lines):
                        next_line = lines[i+1]
                        if next_line.strip() and not next_line.startswith(" "):
                            # Indent it!
                            indent_match = re.match(r"^(\s*)", line)
                            indent = indent_match.group(1) if indent_match else ""
                            new_lines.append(indent + "    " + next_line)
                            modified = True
                            i += 2
                            continue
                new_lines.append(line)
                i += 1

            if modified:
                p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                print(f"Fixed indentation in {p}")
        except (IOError, OSError, UnicodeDecodeError) as e:
            print(f"Error fixing {p}: {e}")

if __name__ == "__main__":
    # Robustly find the repository root
    current_path = Path(__file__).resolve()
    project_root = current_path
    while project_root.name != 'src' and project_root.parent != project_root:
        project_root = project_root.parent
    if project_root.name == 'src':
        project_root = project_root.parent

    fix_broken_indentation(project_root / "src")
    fix_broken_indentation(project_root / "tests")
