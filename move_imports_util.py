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

"""Utility for moving specific standard library imports out of TYPE_CHECKING blocks to runtime."""

from __future__ import annotations
from src.core.base.version import VERSION
import os
import re

__version__ = VERSION

def fix_file(file_path: str) -> None:
    """Move standard library imports from TYPE_CHECKING to top-level."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find if TYPE_CHECKING: block
    pattern = re.compile(r'if TYPE_CHECKING:\s+(?:\s*(?:pass|from|import).*)+', re.MULTILINE)
    
    match = pattern.search(content)
    if not match:
        return

    block = match.group(0)
    lines = block.split('\n')
    
    new_block_lines = []
    extracted_lines = []
    
    runtime_modules = ['dataclasses', 'enum', 'pathlib', 'json', 'logging', 'os', 'sys', 'time', 'datetime', 're', 'argparse', 'typing', 'abc', 'functools', 'collections', 'itertools', 'threading', 'inspect']
    
    started = False
    for line in lines:
        if 'if TYPE_CHECKING:' in line:
            new_block_lines.append(line)
            started = True
            continue
        
        if not started:
            continue
            
        stripped = line.strip()
        if not stripped or stripped == 'pass':
            new_block_lines.append(line)
            continue
            
        # Check if it's an import we want to move out
        is_runtime = False
        # Only move out if it's a standard library import
        if stripped.startswith('from '):
            mod_part = stripped.split(' ')[1]
            if mod_part in runtime_modules:
                is_runtime = True
        elif stripped.startswith('import '):
            mod_part = stripped.split(' ')[1]
            if mod_part in runtime_modules:
                is_runtime = True
        
        if is_runtime:
            extracted_lines.append(stripped)
        else:
            new_block_lines.append(line)
            
    if not extracted_lines:
        return
        
    # Reconstruct
    new_content = content.replace(block, '\n'.join(extracted_lines) + '\n' + '\n'.join(new_block_lines))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Moved imports in {file_path}")

def walk_dir(path: str) -> None:
    """Walk directory to apply import movement fix to all python files."""
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    walk_dir('src')
    walk_dir('tests')