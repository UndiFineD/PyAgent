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

"""Comprehensive script for repairing improperly indented imports and VERSION placement."""

from __future__ import annotations
from src.core.base.version import VERSION
import os
import re

__version__ = VERSION

def fix_all() -> None:
    """Correct import indentation and reposition VERSION imports."""
    target_module = "src.version"
    import_pattern = re.compile(r"^(import \w+|from [\w\.]+ import)")

    for root, dirs, files in os.walk(os.getcwd()):
        if "__pycache__" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except Exception:
                    continue
                
                changed = False
                new_lines = []
                is_inside_block = False
                last_non_empty_indent = ""
                
                for i, line in enumerate(lines):
                    # 1. Fix the version import (SHOULD ALWAYS BE COL 0 AT TOP LEVEL)
                    if f"from {target_module} import VERSION" in line:
                        if not is_inside_block:
                            if line.startswith(" ") or line.startswith("\t"):
                                line = line.lstrip()
                                changed = True
                    
                    # 2. Track block state
                    ls = line.lstrip()
                    if ls.startswith(("def ", "class ", "try:", "except", "finally:", "if ", "for ", "while ", "with ")):
                        is_inside_block = True
                    
                    # Keep track of indentation for non-empty lines
                    m = re.match(r"^(\s+)", line)
                    if m and line.strip():
                        last_non_empty_indent = m.group(1)
                    
                    # 3. Fix imports at col 0 that should be indented
                    if is_inside_block and import_pattern.match(line):
                        # Guess indent
                        indent = ""
                        # Look back for indent
                        for j in range(i-1, -1, -1):
                            if lines[j].strip() and (lines[j].startswith(" ") or lines[j].startswith("\t")):
                                m = re.match(r"^(\s+)", lines[j])
                                if m:
                                    indent = m.group(1)
                                    break
                        if not indent:
                            # Look forward
                            for j in range(i+1, min(i+10, len(lines))):
                                if lines[j].strip() and (lines[j].startswith(" ") or lines[j].startswith("\t")):
                                    m = re.match(r"^(\s+)", lines[j])
                                    if m:
                                        indent = m.group(1)
                                        break
                        if not indent:
                            indent = last_non_empty_indent or "    "
                            
                        line = indent + line
                        changed = True
                    
                    # Reset block state if we see a code line at col 0 that isn't a block keyword or comment
                    if line.strip() and not (line.startswith(" ") or line.startswith("\t")):
                        if not line.startswith(("#", "import", "from")):
                            # Check if it starts a new block
                            if not line.startswith(("def ", "class ", "try:", "except", "finally:", "if ", "for ", "while ", "with ")):
                                is_inside_block = False

                    new_lines.append(line)
                
                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Fixed {path}")

if __name__ == "__main__":
    fix_all()