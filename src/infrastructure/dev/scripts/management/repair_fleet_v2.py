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

"""Script for repairing specific import corruption patterns in the fleet."""

from __future__ import annotations
from src.core.base.version import VERSION
import os
import re

__version__ = VERSION

def repair() -> None:
    """Repair multiple types of import and string formatting corruption."""
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 1. Fix "from X from Y import Z"
                    content = re.sub(r"from ([\w.]+) from ([\w.]+) import ([\w, ]+)", r"from \1 import \3\nfrom \2 import \3", content)
                    # Wait, that might not be right. Let's look at the error:
                    # from __future__ from functools import lru_cache
                    # Probably meant:
                    # from __future__ import annotations
                    # from functools import lru_cache
                    
                    content = content.replace("from __future__ from functools import lru_cache", "from __future__ import annotations\nfrom functools import lru_cache")
                    content = content.replace("from typing from functools import lru_cache", "from typing import Any, Dict, List\nfrom functools import lru_cache")
                    content = content.replace("from dataclasses from functools import lru_cache", "from dataclasses import dataclass\nfrom functools import lru_cache")
                    content = content.replace("from .CodeLanguage from functools import lru_cache", "from .CodeLanguage import CodeLanguage\nfrom functools import lru_cache")
                    content = content.replace("from src.core.base.BaseAgent from functools import lru_cache", "from src.core.base.BaseAgent import BaseAgent\nfrom functools import lru_cache")
                    content = content.replace("from fastapi from functools import lru_cache", "from fastapi import FastAPI\nfrom functools import lru_cache")

                    # 2. Fix nested quotes in logging
                    # logging.debug(f'Fleet Debug: 'Section {i}')"')
                    content = re.sub(r"logging\.debug\(f'Fleet Debug: '(.*)'\b", r"logging.debug(f'Fleet Debug: \"\1\"", content)
                    
                    if content != original_content:
                        print(f"Repaired {path}")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error repairing {path}: {e}")

if __name__ == "__main__":
    repair()