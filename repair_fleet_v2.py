import os
import re

def repair():
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
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
                    content = content.replace("from src.classes.base_agent from functools import lru_cache", "from src.classes.base_agent.agent import BaseAgent\nfrom functools import lru_cache")
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
