#!/usr/bin/env python3
"""
Batch fixer for PyAgent: Remove stray double quotes in the middle of identifiers or words, and fix lines ending with a stray quote.
- Fixes cases like pay"loads -> payloads, scan_content"(content) -> scan_content(content), etc.
- Comments out lines ending with a stray quote if not a docstring.
"""
import re
from pathlib import Path

TARGET_DIRS = [
    Path('src/logic/agents'),
    Path('src/observability/errors'),
]

# Pattern for a stray quote in the middle of a word/identifier
STRAY_QUOTE_IN_WORD = re.compile(r'([a-zA-Z0-9_])"([a-zA-Z0-9_])')
# Pattern for a line ending with a stray quote (not triple quote)
STRAY_QUOTE_END = re.compile(r'^(.*[^"\'])"\s*$')
TRIPLE_QUOTE_START = re.compile(r'^[\s]*["\']{3}')


def fix_file(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for i, line in enumerate(lines):
        # Remove stray quote in the middle of a word/identifier
        fixed = STRAY_QUOTE_IN_WORD.sub(r'\1\2', line)
        # If line ends with a stray quote and is not a docstring, comment it out
        if STRAY_QUOTE_END.match(fixed) and not TRIPLE_QUOTE_START.match(fixed):
            new_lines.append('# ' + fixed.rstrip('"').rstrip())
            continue
        new_lines.append(fixed)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f"Fixed stray quote in: {path}")

if __name__ == "__main__":
    for target_dir in TARGET_DIRS:
        for pyfile in target_dir.rglob('*.py'):
            fix_file(pyfile)
    print("Batch stray quote in word fix complete.")
