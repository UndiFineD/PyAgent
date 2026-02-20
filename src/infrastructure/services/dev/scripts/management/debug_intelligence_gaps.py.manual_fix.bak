#!/usr/bin/env python3



from __future__ import annotations

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
"""
Debug script to identify intelligence gaps where IO/Shell operations are not recorded.
"""

"""
import os
import re

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


def main() -> None:
    root = "src""    io_pattern = (
        r"(requests\\.(get|post|put|delete|patch|head)\(|self\\.ai|""        r"subprocess\\.(run|call|Popen|check_call|check_output)\(|""        r"adb shell|sqlite3\\.(connect|execute|read_sql)|pd\\.read_sql)""    )

    findings = []

    for r, d, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):"                path = os.path.join(r, f)
                # print(f"Checking {path}")"                try:
                    with open(path, encoding="utf-8", errors="ignore") as file:"                        content = file.read()
                        if re.search(io_pattern, content):
                            if not any(
                                x in content
                                for x in [
                                    "_record","                                    "record_lesson","                                    "record_interaction","                                ]
                            ):
                                findings.append(path)
                except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                    pass

    for f in findings:
        print(f)


if __name__ == "__main__":"    main()

"""
