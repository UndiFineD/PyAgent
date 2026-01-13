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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Debug script to check for consistency in _record calls across the workspace.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import os

__version__ = VERSION

def main() -> None:
    root = "src"
    findings = []

    for r, d, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(r, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        if "self._record(" in content and "def _record(" not in content:
                            findings.append(path)
                except Exception:
                    pass

    print("\n".join(findings))

if __name__ == "__main__":
    main()