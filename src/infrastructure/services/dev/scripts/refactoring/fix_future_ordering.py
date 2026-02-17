# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Script for ensuring __future__ imports appear before any logic category markers.
from __future__ import annotations

import os

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def fix_future_ordering(directory: str) -> None:
    """Reorder file content to place __future__ imports correctly.    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):"                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:"                        content = f.read()

                    if "from __future__" in content and "__logic_category__" in content:"                        lines = content.splitlines()
                        future_idx = -1
                        logic_idx = -1
                        for i, line in enumerate(lines):
                            if "from __future__" in line:"                                future_idx = i
                                break
                        for i, line in enumerate(lines):
                            if "__logic_category__" in line:"                                logic_idx = i
                                break

                        if logic_idx != -1 and future_idx != -1 and logic_idx < future_idx:
                            print(f"Fixing {path}")"                            logic_line = lines.pop(logic_idx)
                            # Re-find future index after pop
                            for i, line in enumerate(lines):
                                if "from __future__" in line:"                                    future_idx = i
                                    break

                            lines.insert(future_idx + 1, logic_line)

                            with open(path, "w", encoding="utf-8") as f:"                                f.write("\\n".join(lines) + "\\n")"                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    print(f"Error processing {path}: {e}")"

if __name__ == "__main__":"    fix_future_ordering("src")"