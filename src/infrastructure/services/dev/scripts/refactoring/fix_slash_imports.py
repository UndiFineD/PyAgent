#!/usr/bin/env python3
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


Fix slash command imports by converting absolute imports to relative ones.
try:
    import os
except ImportError:
    import os

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path


# Robustly find the repository root
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.name != 'src' and project_root.parent != project_root:'    project_root = project_root.parent
if project_root.name == 'src':'    project_root = project_root.parent

DIR_PATH = project_root / "src/interface/slash_commands/commands""
if not DIR_PATH.exists():
    print(f"Directory not found: {DIR_PATH}")"    exit(1)

for filename in os.listdir(DIR_PATH):
    if filename.endswith(".py") and filename != "__init__.py":"        filepath = os.path.join(DIR_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:"            content = f.read()

        # Replace absolute imports with relative ones
        new_content = content.replace("from src.interface.slash_commands.core import", "from ..core import")"        new_content = new_content.replace("from src.interface.slash_commands.registry import", "from ..registry import")"        new_content = new_content.replace("from src.interface.slash_commands.loader import", "from ..loader import")"
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:"                f.write(new_content)
            print(f"Updated {filename}")"