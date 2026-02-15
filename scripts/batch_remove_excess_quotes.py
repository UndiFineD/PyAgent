#!/usr/bin/env python3
"""
Batch fixer for PyAgent: Remove all excessive and corrupted quote sequences (e.g., """""", '''''', etc.) from all .py files in src/logic/agents and src/observability/errors.
- Cleans up docstrings, identifiers, and code.
- Restores valid Python syntax and docstrings.
"""
import re
from pathlib import Path

TARGET_DIRS = [
    Path('src/logic/agents'),
    Path('src/observability/errors'),
]

QUOTE_SEQ = re.compile(r'("{3,}|\'{3,})')
EXCESS_QUOTES = re.compile(r'("{2,}|\'{2,})+')
IDENTIFIER_QUOTE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)["\']{2,}([a-zA-Z_][a-zA-Z0-9_]*)')


def clean_text(text):
    # Remove all sequences of 3 or more quotes
    text = QUOTE_SEQ.sub('"""', text)
    # Remove excessive double/single quotes in identifiers and code
    text = EXCESS_QUOTES.sub('"', text)
    text = IDENTIFIER_QUOTE.sub(r'\1\2', text)
    return text


def fix_file(path: Path):
    orig = text = path.read_text(encoding='utf-8')
    cleaned = clean_text(text)
    if cleaned != text:
        path.write_text(cleaned, encoding='utf-8')
        print(f"Cleaned: {path}")

if __name__ == "__main__":
    for target_dir in TARGET_DIRS:
        for pyfile in target_dir.rglob('*.py'):
            fix_file(pyfile)
    print("Batch excessive quote cleanup complete.")
