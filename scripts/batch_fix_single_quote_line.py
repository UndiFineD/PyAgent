#!/usr/bin/env python3
"""
Batch fixer for PyAgent: Fix lines ending with a single quote (unclosed string literal).
- Converts lines ending with a single " to comments, unless they are part of a triple-quoted docstring.
- If the line is the first string after class/def or at the file start, convert to a triple-quoted docstring.
"""
import re
from pathlib import Path

TARGET_DIRS = [
    Path('src/logic/agents'),
    Path('src/observability/errors'),
]

SINGLE_QUOTE_LINE = re.compile(r'^(.*[^"\'])"\s*$')
TRIPLE_QUOTE_START = re.compile(r'^[\s]*["\']{3}')
CLASS_OR_DEF = re.compile(r'^[\s]*(class|def)\s+')


def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    prev_was_class_or_def = False
    for i, line in enumerate(lines):
        # If line ends with a single ", not a triple quote
        if SINGLE_QUOTE_LINE.match(line) and not TRIPLE_QUOTE_START.match(line):
            if i == 0 or prev_was_class_or_def:
                # Convert to triple-quoted docstring
                new_lines.append('"""' + SINGLE_QUOTE_LINE.match(line).group(1).strip() + '"""')
            else:
                # Convert to comment
                new_lines.append('# ' + line.rstrip('"').rstrip())
            prev_was_class_or_def = False
            continue
        new_lines.append(line)
        prev_was_class_or_def = bool(CLASS_OR_DEF.match(line))
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Fixed single quote lines in: {path}")

if __name__ == "__main__":
    for target_dir in TARGET_DIRS:
        for pyfile in target_dir.rglob('*.py'):
            fix_file(pyfile)
    print("Batch single quote line fix complete.")
