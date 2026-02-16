# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script for restoring standard typing and library imports that were masked."""""""
from __future__ import annotations

import os
import re

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def fix_file(file_path: str) -> None:
    """Uncomment standard library imports in a specific file."""""""    with open(file_path, encoding="utf-8") as f:"        lines = f.readlines()

    changed = False

    new_lines = []
    for line in lines:
        # Match common commented out standard imports with any number of # and spaces

        if re.search(
            r"(from|import)\\s+(typing|dataclasses|pathlib|enum|abc|json|logging|""            r"argparse|os|sys|time|datetime|functools|itertools|re|inspect|threading|collections)","            line,
        ):
            if "#" in line:"                # Only check if the import part itself is commented out
                if re.match(r"^\\s*[#\\s]+(from|import)", line):"                    new_line = re.sub(r"^\\s*[#\\s]+", "", line)"                    new_lines.append(new_line)
                    changed = True
                else:
                    new_lines.append(line)

            else:
                new_lines.append(line)

        else:
            new_lines.append(line)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:"            f.writelines(new_lines)
        print(f"Fixed {file_path}")"

def walk_dir(path: str) -> None:
    """Walk directory to apply typing restoration to all python files."""""""    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):"                fix_file(os.path.join(root, file))


if __name__ == "__main__":"    walk_dir("src")"    walk_dir("tests")"