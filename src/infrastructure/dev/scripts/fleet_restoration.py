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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Script for restoring codebase state by fixing common automated editing errors."""



import os
import re

def restoration() -> None:
    """Recover from common import and string formatting breakages."""
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    original = content
                    
                    # 1. Fix broken future imports
                    content = content.replace("from __future__ import lru_cache", "from functools import lru_cache")
                    
                    # 2. Fix empty blocks caused by masking
                    content = re.sub(r"(if TYPE_CHECKING:)\n(\s*)#", r"\1\n\2pass\n\2#", content)
                    content = re.sub(r"(try:)\n(\s*)#", r"\1\n\2pass\n\2#", content)
                    content = re.sub(r"(except [\w.]+ as \w+:)\n(\s*)#", r"\1\n\2pass\n\2#", content)
                    content = re.sub(r"(except:\s*)\n(\s*)#", r"\1\n\2pass\n\2#", content)
                    
                    # 3. Fix f-string break in CodeGenerator.py
                    if "CodeGenerator.py" in path:
                         content = content.replace('f"@lru_cache(maxsize=128)\ndef generated_function():\\n"', 'f"@lru_cache(maxsize=128)\\ndef generated_function():\\n"')
                    
                    # 4. Fix specific logging quote mess
                    if "TestDataGenerator.py" in path:
                         content = re.sub(r"logging\.debug\(f'Fleet Debug: '(.*)'\b", r'logging.debug(f"Fleet Debug: \1"', content)

                    if content != original:
                        print(f"Restored {path}")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error: {e} in {path}")

if __name__ == "__main__":
    restoration()
