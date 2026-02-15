#!/usr/bin/env python3
"""
Batch fixer for src/observability/errors:
- Comments out lines at the top of the file (first 40 lines) with a colon that are not valid Python (e.g., AUTHOR: ...).
- Comments out long prose lines or standalone sentences at the top of the file.
- Designed to be run after previous fixers.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Regex for lines with colon but not valid Python
COLON_LINE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_ ]*):\s+(.+)$')
# Regex for valid Python lines (import, def, class, from, comment, docstring)
VALID_PYTHON = re.compile(r'^(\s*#|\s*"""|\s*from |\s*import |\s*class |\s*def |\s*@|\s*$)')
# Regex for prose/sentence lines (not code, not comment, not import)
PROSE_LINE = re.compile(r'^[A-Z][^#"\']{10,}[\.]$')

def comment_line(line):
    if line.strip().startswith('#'):
        return line
    return '# ' + line

def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for i, line in enumerate(lines):
        # Only operate on the first 40 lines
        if i < 40:
            # Comment colon lines not valid Python
            if COLON_LINE.match(line) and not VALID_PYTHON.match(line):
                new_lines.append(comment_line(line))
                continue
            # Comment prose/sentence lines
            if PROSE_LINE.match(line) and not VALID_PYTHON.match(line):
                new_lines.append(comment_line(line))
                continue
        new_lines.append(line)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Commented colon/prose lines in: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Batch colon/prose line commenting complete.")
