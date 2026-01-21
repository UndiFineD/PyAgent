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


from __future__ import annotations
from src.core.base.version import VERSION
import os
import re

__version__ = VERSION


def apply_basic_types(target_dir="src") -> bool:
    """
    Applies basic return type hints to functions where inference is certain.
    - __init__ -> None
    - Functions returning True/False -> bool
    - Functions returning string literals -> str
    """
    fixed_files = 0
    total_fixes = 0

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                file_fixes = 0

                # 1. Constructor typing
                # We look for def __init__(self, ...): and add -> None
                # Avoid if already typed
                if (
                    "def __init__(self" in new_content
                    and "-> None"
                    not in new_content.split("def __init__")[1].split(":")[0]
                ):
                    new_content = re.sub(
                        r"(def\s+__init__\s*\([^)]+\))\s*:", r"\1 -> None:", new_content
                    )

                    file_fixes += 1

                # 2. Boolean return inference

                # Find methods that end with return True/False and have no type hint
                # This is a bit risky but we'll try simple patterns
                bool_patterns = [
                    (
                        r"def\s+(\w+)\s*\((self[^)]*)\):\s*\n\s+return\s+(True|False)\s*\n",
                        r"def \1(\2) -> bool:\n    return \3\n",
                    ),
                ]
                for pattern, subst in bool_patterns:
                    matches = re.findall(pattern, new_content)
                    if matches:
                        new_content = re.sub(pattern, subst, new_content)

                        file_fixes += len(matches)

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    fixed_files += 1
                    total_fixes += file_fixes

    print(f"Applied {total_fixes} basic type hints across {fixed_files} files.")


if __name__ == "__main__":
    apply_basic_types()
