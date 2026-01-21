import os
import re

COPYRIGHT_BLOCK = """# Copyright 2026 PyAgent Authors
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


def fix_header(lines: list[str], filename: str = "") -> list[str]:
    shebang = None
    _future = "from __future__ import annotations\n"
    _v_import = "from src.core.base.lifecycle.version import VERSION\n"
    _v_assign = "__version__ = VERSION\n"

    # Skip version injection for the version file itself
    skip_version = "version.py" in filename.lower()

    remaining = []

    # 1. Strip all "header-like" items to re-insert them later
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#!") and not shebang:
            shebang = line
            continue
        # Skip existing copyright blocks to avoid duplicates
        if stripped.startswith("# Copyright") or stripped.startswith(
            "# Licensed under the Apache"
        ):
            continue
        if "http://www.apache.org/licenses/LICENSE-2.0" in stripped:
            continue
        if "Unless required by applicable law or agreed to in writing" in stripped:
            continue
        if (
            'distributed under the License is distributed on an "AS IS" BASIS'
            in stripped
        ):
            continue
        if (
            "See the License for the specific language governing permissions"
            in stripped
        ):
            continue

        if re.match(r"^from\s+__future__\s+import\s+annotations", stripped):
            continue
        if re.match(r"^from\s+src\.core\.base\.version\s+import\s+VERSION", stripped):
            continue
        if re.match(r"^__version__\s*=\s*VERSION", stripped):
            continue
        remaining.append(line)

    # Clean up leading blanks
    while remaining and not remaining[0].strip():
        remaining.pop(0)

    new_lines = []
    if shebang:
        new_lines.append(shebang)

    # Insert Copyright Block
    new_lines.append(COPYRIGHT_BLOCK + "\n")

    # Insert Future Import
    new_lines.append(_future + "\n")

    # 2. Add Docstring if one exists at the top of remaining
    idx = 0
    if idx < len(remaining) and (
        remaining[idx].strip().startswith('"""')
        or remaining[idx].strip().startswith("'''")
    ):
        start_quote = remaining[idx].strip()[:3]
        new_lines.append(remaining[idx])
        if remaining[idx].strip().count(start_quote) == 1:
            idx += 1

            while idx < len(remaining) and start_quote not in remaining[idx]:
                new_lines.append(remaining[idx])
                idx += 1

            if idx < len(remaining):
                new_lines.append(remaining[idx])
                idx += 1
        else:
            idx += 1
        new_lines.append("\n")

    # 3. Add Versioning
    if not skip_version:
        new_lines.append(_v_import)
        new_lines.append(_v_assign + "\n")

    # 4. Add the rest
    while idx < len(remaining):
        new_lines.append(remaining[idx])
        idx += 1

    return new_lines


def process_directory(directory: str) -> None:
    for root, dirs, files in os.walk(directory):
        # Skip hidden and cache dirs

        if ".git" in root or "__pycache__" in root or ".venv" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                # Skip the script itself
                if "fix_headers.py" in file:
                    continue

                print(f"Processing {filepath}")
                try:
                    with open(filepath, encoding="utf-8") as f:
                        lines = f.readlines()

                    if not lines:
                        continue

                    new_lines = fix_header(lines, filename=file)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    base_path = r"c:\DEV\PyAgent\src"
    process_directory(base_path)
    # Also process root files
    root_files = [f for f in os.listdir(r"c:\DEV\PyAgent") if f.endswith(".py")]
    for f in root_files:
        filepath = os.path.join(r"c:\DEV\PyAgent", f)
        print(f"Processing root file {filepath}")
        try:
            with open(filepath, encoding="utf-8") as file_handle:
                lines = file_handle.readlines()
            if lines:
                new_lines = fix_header(lines, filename=f)
                with open(filepath, "w", encoding="utf-8") as file_handle:
                    file_handle.writelines(new_lines)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
