#!/usr/bin/env python3
"""
Batch fixer for src/observability/errors:
- Comments out lines like '[Brief Summary]', 'Brief Summary', or any bracketed/standalone summary lines.
- Comments out any line at the top of the file that is not valid Python (not import, docstring, or comment).
- Designed to be run after previous fixers.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Regex for bracketed or summary lines
BRACKETED_LINE = re.compile(r'^\s*\[.*?\]\s*$')
SUMMARY_LINE = re.compile(r'^\s*Brief Summary\s*$')
# Regex for lines that are a single word/phrase (not valid Python)
SINGLE_PHRASE = re.compile(r'^\s*[A-Za-z_][A-Za-z0-9_ ]*\s*$')
# Regex for valid Python lines (import, docstring, comment, class/def)
VALID_PYTHON = re.compile(r'^(\s*#|\s*"""|\s*from |\s*import |\s*class |\s*def |\s*@|\s*$)')

def comment_line(line):
    if line.strip().startswith('#'):
        return line
    return '# ' + line

def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for i, line in enumerate(lines):
        # Comment bracketed or summary lines
        if BRACKETED_LINE.match(line) or SUMMARY_LINE.match(line):
            new_lines.append(comment_line(line))
            continue
        # Comment single phrase lines at the top (first 30 lines)
        if i < 30 and SINGLE_PHRASE.match(line) and not VALID_PYTHON.match(line):
            new_lines.append(comment_line(line))
            continue
        new_lines.append(line)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Commented bracketed/summary lines in: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Batch bracketed/summary line commenting complete.")
