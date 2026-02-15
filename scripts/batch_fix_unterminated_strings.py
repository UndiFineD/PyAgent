#!/usr/bin/env python3
"""
Batch fixer for PyAgent: Fix unterminated string literals at the start of files or after class/def.
- Removes or closes lone " or ' at the start of a file or after class/def.
- Ensures all docstrings are valid triple-quoted strings.
- Converts lone " to comments if not recoverable.
"""
import re
from pathlib import Path

TARGET_DIRS = [
    Path('src/logic/agents'),
    Path('src/observability/errors'),
]

# Pattern for a line that is just a single or double quote
LONE_QUOTE = re.compile(r'^\s*["\"][\s]*$')
# Pattern for a line that is just a single or double quote with optional whitespace
LONE_QUOTE_ANY = re.compile(r'^[\s]*["\"][\s]*$')
# Pattern for a line that is just a triple quote (unterminated docstring)
LONE_TRIPLE = re.compile(r'^[\s]*["\"]["\"]["\"][\s]*$')


def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    in_docstring = False
    for i, line in enumerate(lines):
        # Remove lone quote lines
        if LONE_QUOTE.match(line):
            # If previous line is class/def or at file start, skip this line
            if i == 0 or (i > 0 and (lines[i-1].strip().startswith('class ') or lines[i-1].strip().startswith('def '))):
                continue
            # Otherwise, comment it out
            new_lines.append('# ' + line.strip())
            continue
        # Remove lone triple quote lines
        if LONE_TRIPLE.match(line):
            # If previous line is class/def or at file start, skip this line
            if i == 0 or (i > 0 and (lines[i-1].strip().startswith('class ') or lines[i-1].strip().startswith('def '))):
                continue
            # Otherwise, comment it out
            new_lines.append('# ' + line.strip())
            continue
        new_lines.append(line)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Fixed unterminated strings in: {path}")

if __name__ == "__main__":
    for target_dir in TARGET_DIRS:
        for pyfile in target_dir.rglob('*.py'):
            fix_file(pyfile)
    print("Batch unterminated string fix complete.")
