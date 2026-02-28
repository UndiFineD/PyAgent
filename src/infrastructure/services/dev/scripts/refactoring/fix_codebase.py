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
Utility to repair corrupted source files by uncommenting essential system imports.
Part of the Fleet Healer autonomous recovery pattern.
"""

from __future__ import annotations

import os
import re

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def uncomment_lines(root_dir: str) -> None:
    # Regex to catch commented-out essential imports
    p_from = re.compile(
        r"^\s*#\s*(from\s+(?:typing|dataclasses|__future__|pathlib|datetime|"
        r"abc|functools|enum|typing_extensions)\s+import\s+)",
        re.M,
    )
    p_import = re.compile(
        r"^\s*#\s*(import\s+(?:os|json|logging|re|sys|time|math|hashlib|shutil|"
        r"subprocess|tempfile|glob|uuid|collections|random|inspect|threading|"
        r"queue|socket|urllib|traceback|ast|argparse|pathlib))\b",
        re.M,
    )

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()

                    new_content = p_from.sub(r"\1", content)
                    new_content = p_import.sub(r"\1", new_content)

                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Fixed: {filepath}")
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    print(f"Error fixing {filepath}: {e}")


if __name__ == "__main__":
    uncomment_lines("src/classes")
