#!/usr/bin/env python3
"""
Aggressive batch cleaner for src/observability/errors:
- Removes all injected quote sequences (e.g., """""", '''''', etc.) from identifiers, types, and strings.
- Repairs unterminated triple-quoted strings and docstrings.
- Cleans up unmatched parentheses/braces caused by corruption.
- Designed for repeated runs and large-scale corruption.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Remove all sequences of 3 or more quotes (single or double)
QUOTE_SEQ = re.compile(r'(["\"])\1{2,}')

# Remove quote sequences in identifiers, types, and strings
IDENTIFIER_QUOTE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)["\"]{3,}([a-zA-Z_][a-zA-Z0-9_]*)')
TYPE_QUOTE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)["\"]{3,}(\[.*?\])')
STRING_QUOTE = re.compile(r'"([a-zA-Z0-9_ ]*)["\"]{3,}([a-zA-Z0-9_ ]*)"')

# Remove unterminated triple-quoted strings (replace with empty string)
UNTERMINATED_TRIPLE = re.compile(r'"""[^"]*$|\'\'\'[^"]*$')

# Remove unmatched parentheses/braces at line ends
UNMATCHED_PAREN = re.compile(r'([\(\{\[])[^\)\}\]]*$')

# Remove any trailing quote sequences at line ends
TRAILING_QUOTES = re.compile(r'["\"]{3,}$')

# Remove any leading quote sequences at line starts
LEADING_QUOTES = re.compile(r'^["\"]{3,}')

def clean_text(text):
    orig = text
    # Remove all sequences of 3 or more quotes
    text = QUOTE_SEQ.sub('', text)
    # Remove quote sequences in identifiers, types, and strings
    text = IDENTIFIER_QUOTE.sub(r'\1\2', text)
    text = TYPE_QUOTE.sub(r'\1\2', text)
    text = STRING_QUOTE.sub(lambda m: f'"{m.group(1)}{m.group(2)}"', text)
    # Remove unterminated triple-quoted strings
    text = UNTERMINATED_TRIPLE.sub('', text)
    # Remove unmatched parens/braces at line ends
    text = UNMATCHED_PAREN.sub('', text)
    # Remove trailing and leading quote sequences
    text = TRAILING_QUOTES.sub('', text)
    text = LEADING_QUOTES.sub('', text)
    return text

def fix_file(path: Path):
    text = path.read_text(encoding='utf-8')
    cleaned = clean_text(text)
    if cleaned != text:
        path.write_text(cleaned, encoding='utf-8')
        print(f"Cleaned: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Aggressive quote and corruption cleaning complete.")
