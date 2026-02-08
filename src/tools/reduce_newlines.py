#!/usr/bin/env python3
import os
from pathlib import Path

def reduce_newlines(directory: Path):
    for p in directory.rglob("*.py"):
        if not p.is_file():
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        # Replace 3 or more newlines with 2
        import re
        new_content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)
        if new_content != content:
            p.write_text(new_content, encoding="utf-8")
            print(f"Reduced newlines in {p}")

if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/external_candidates/auto")
    reduce_newlines(target)
