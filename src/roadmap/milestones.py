#!/usr/bin/env python3
"""Milestones module for PyAgent."""
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

from pathlib import Path
from typing import Union


async def create(path: Union[str, Path], items: list[str]) -> None:
    """Create a markdown file at *path* with a list of *items* as milestones."""
    p = Path(path)
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Technology Roadmap\n\n")
        for item in items:
            f.write(f"- {item}\n")
    return
