#!/usr/bin/env python3
"""Remove single leading space before top-level 'from' or 'import' lines in src/."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "src"
count = 0
for p in root.rglob("*.py"):
    try:
        txt = p.read_text(encoding="utf-8")
    except Exception:
        continue
    lines = txt.splitlines(True)
    changed = False
    # track previous non-empty, non-comment line to avoid modifying indented blocks
    prev_nonblank = ""
    for i, line in enumerate(lines):
        stripped = line.lstrip(" \t")
        indent_len = len(line) - len(stripped)
        if stripped.startswith(("from ", "import ")) and indent_len > 0:
            # avoid modifying imports that are inside an indented block (prev line ends with ':')
            if prev_nonblank.strip().endswith(":"):
                pass
            else:
                lines[i] = stripped
                changed = True
                count += 1
        if line.strip() and not line.strip().startswith("#"):
            prev_nonblank = line
    if changed:
        p.write_text("".join(lines), encoding="utf-8")
print(f"Fixed {count} lines in src files")
