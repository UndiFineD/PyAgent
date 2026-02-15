#!/usr/bin/env python3
"""
Batch fixer for src/observability/errors:
- Comments out lines at the top of the file (first 50 lines) that are just a single word and colon (e.g., USAGE:).
- Comments out lines starting with a dash or bullet (e.g., - ...).
- Comments out any line not valid Python, comment, or docstring.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Regex for single word and colon (e.g., USAGE:)
SINGLE_COLON = re.compile(r'^\s*[A-Za-z_][A-Za-z0-9_ ]*:\s*$')
# Regex for lines starting with dash or bullet
BULLET_LINE = re.compile(r'^\s*[-•]\s+')
# Regex for valid Python lines (import, def, class, from, comment, docstring)
VALID_PYTHON = re.compile(r'^(\s*#|\s*"""|\s*from |\s*import |\s*class |\s*def |\s*@|\s*$)')

def comment_line(line):
    if line.strip().startswith('#'):
        return line
    return '# ' + line

def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for i, line in enumerate(lines):
        # Only operate on the first 50 lines
        if i < 50:
            # Comment single word and colon lines
            if SINGLE_COLON.match(line):
                new_lines.append(comment_line(line))
                continue
            # Comment bullet/dash lines
            if BULLET_LINE.match(line):
                new_lines.append(comment_line(line))
                continue
        new_lines.append(line)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Commented usage/bullet lines in: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Batch usage/bullet line commenting complete.")
