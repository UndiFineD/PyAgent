#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Compile Mermaid/PlantUML diagrams into SVG files."""

from __future__ import annotations

import subprocess
from pathlib import Path

diagram_dir = Path("docs/architecture")


def compile_diagrams() -> None:
    """Produce SVGs for each .mmd file in the architecture directory."""
    for path in diagram_dir.glob("*.mmd"):
        out = path.with_suffix(".svg")
        # assume `mmdc` (Mermaid CLI) is installed
        subprocess.run(["mmdc", "-i", str(path), "-o", str(out)], check=True)  # noqa: S603 S607
        print(f"compiled {path} -> {out}")


if __name__ == "__main__":
    compile_diagrams()
