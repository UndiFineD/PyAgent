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

"""Script for standardizing the position of __future__ imports at the top of files."""

from __future__ import annotations
from src.core.base.Version import VERSION
import os

__version__ = VERSION

src_path = r"c:\DEV\PyAgent\src"
for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "from __future__ import annotations" in content:
                lines = content.splitlines()
                annotation_line = ""
                other_lines = []
                for line in lines:
                    if "from __future__ import annotations" in line:
                        annotation_line = line
                    else:
                        other_lines.append(line)

                if annotation_line:
                    # Find insertion point (after shebang/encoding)
                    insert_idx = 0
                    if other_lines and other_lines[0].startswith("#!"):
                        insert_idx = 1
                    if len(other_lines) > insert_idx and (
                        "coding:" in other_lines[insert_idx]
                        or "-*-" in other_lines[insert_idx]
                    ):
                        insert_idx += 1

                    other_lines.insert(insert_idx, "from __future__ import annotations")
                    new_content = "\n".join(other_lines) + (
                        "\n" if content.endswith("\n") else ""
                    )

                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Repositioned: {path}")
