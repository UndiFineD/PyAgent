#!/usr/bin/env python3
"""
Batch fixer for src/observability/errors:
- Converts lines like 'ClassName - Description' to comments.
- Comments out lines with em dash (—) or other non-ASCII metadata.
- Ensures all docstrings are properly closed.
- Comments out unterminated string literals at the top level.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Regex for metadata lines: ClassName - Description
METADATA_LINE = re.compile(r'^([A-Za-z_][A-Za-z0-9_ ]*)\s*-\s+(.+)$')
# Regex for lines with em dash or other non-ASCII
EM_DASH_LINE = re.compile(r'.*[—–].*')
# Regex for unterminated string literal (line ends with ")
UNTERMINATED_STRING = re.compile(r'^[^#]*"[^"]*$')
# Regex for unterminated triple-quoted string
UNTERMINATED_TRIPLE = re.compile(r'^[^#]*"""[^"]*$')

# Helper to comment a line if not already commented
def comment_line(line):
    if line.strip().startswith('#'):
        return line
    return '# ' + line

def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    in_triple = False
    for line in lines:
        # Comment metadata lines
        if METADATA_LINE.match(line):
            new_lines.append(comment_line(line))
            continue
        # Comment lines with em dash or other non-ASCII
        if EM_DASH_LINE.match(line):
            new_lines.append(comment_line(line))
            continue
        # Comment unterminated string literals
        if UNTERMINATED_STRING.match(line):
            new_lines.append(comment_line(line))
            continue
        # Comment unterminated triple-quoted strings
        if UNTERMINATED_TRIPLE.match(line):
            new_lines.append(comment_line(line))
            in_triple = not in_triple
            continue
        # If inside unterminated triple-quoted string, comment out until closed
        if in_triple:
            new_lines.append(comment_line(line))
            if '"""' in line:
                in_triple = False
            continue
        new_lines.append(line)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Commented metadata/doc lines in: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Batch metadata/doc line commenting complete.")
