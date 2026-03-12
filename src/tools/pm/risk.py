#!/usr/bin/env python3
"""KPI computation functions for PyAgent."""
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


def read_matrix(path: str) -> list[dict[str, str]]:
    """Read a markdown-based risk matrix and return a list of dictionaries.

    The initial implementation is deliberately naive: it only returns the
    first line as a single-entry dictionary.  Real parsing will come later.
    """
    lines = open(path, encoding="utf-8").read().splitlines()
    if not lines:
        return []
    # naive parse: strip any leading list marker and parse key/value
    line = lines[0].lstrip("- ")
    result: dict[str, str] = {}
    if ":" in line:
        k, v = line.split(":", 1)
        result[k.strip()] = v.strip()
    return [result]
