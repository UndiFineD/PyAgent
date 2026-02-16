#!/usr/bin/env python3
"""
Batch fixer for corrupted type annotations and string literals in src/observability/errors.
- Fixes patterns like set[str], list[str], etc.
- Fixes corrupted string literals like "patte"""rn_match", "di"""scord", etc.
- Repairs docstrings split by injected quote sequences.
- Designed to be idempotent and safe for repeated runs.
"""
import re
from pathlib import Path

TARGET_DIR = Path('src/observability/errors')

# Patterns to fix
TYPE_CORRUPTIONS = [
    (re.compile(r'se"{6}t\[str\]'), 'set[str]'),
    (re.compile(r'lis"{6}t\[str\]'), 'list[str]'),
    (re.compile(r'dict\[str, se"{6}t\[str\]\]'), 'dict[str, set[str]]'),
    (re.compile(r'dict\[str, lis"{6}t\[str\]\]'), 'dict[str, list[str]]'),
    (re.compile(r'Error"{6}Budget'), 'ErrorBudget'),
    (re.compile(r'ErrorCategory\."{6}IM"{6}PORT'), 'ErrorCategory.IMPORT'),
    (re.compile(r'ErrorCategory\.SYNTAX'), 'ErrorCategory.SYNTAX'),
    (re.compile(r'ErrorCategory\.VALUE'), 'ErrorCategory.VALUE'),
]

STRING_CORRUPTIONS = [
    (re.compile(r'"patte"{3}rn"{6}_match"'), '"pattern_match"'),
    (re.compile(r'"di"{3}sc"{6}ord"'), '"discord"'),
    (re.compile(r'"new"{3}re"{6}lic"'), '"newrelic"'),
    (re.compile(r'IN"{3}FO"{6}\s*=\s*1'), 'INFO = 1'),
]

# Remove injected quote sequences in docstrings
DOCSTRING_CORRUPTION = re.compile(r'"{3,}[^\n]*?"{3,}')

# Fixes for attribute assignments with corrupted quotes
ATTR_CORRUPTION = [
    (re.compile(r'description: st"{3}r "{6}= ""'), 'description: str = ""'),
    (re.compile(r'occurrences: i"{3}nt"{6}\s*=\s*0'), 'occurrences: int = 0'),
]

# Fixes for corrupted function/class calls
FUNC_CALL_CORRUPTION = [
    (re.compile(r'self\.branch_errors\[branch"{6}\]'), 'self.branch_errors[branch]'),
    (re.compile(r'self\.branch_errors: dict\[str, se"{6}t\[str\]\] = \{\}'), 'self.branch_errors: dict[str, set[str]] = {}'),
    (re.compile(r'self\.budgets: dict\[str, Error"{6}Budget\] = \{\}'), 'self.budgets: dict[str, ErrorBudget] = {}'),
    (re.compile(r'self\.file_dependencies: dict\[str, lis"{6}t\[str\]\] = \{\}'), 'self.file_dependencies: dict[str, list[str]] = {}'),
    (re.compile(r'self\.file_dependencies\["{6}file\]'), 'self.file_dependencies[file]'),
    (re.compile(r'self\.\"{6}system = system'), 'self.system = system'),
    (re.compile(r'mai"{3}n\("{6}\)'), 'main()'),
    (re.compile(r'base_name = name\[:-10\]  # len\(\'.errors.md'\)'), 'base_name = name[:-10]  # len(.errors.md)'),
    (re.compile(r'if not self.file_path.name.endswith\(".err"{6}ors.md"\):'), 'if not self.file_path.name.endswith(".errors.md"):'),
    (re.compile(r'name = self.fi"{6}le_path.name'), 'name = self.file_path.name'),
]

# Fixes for corrupted enum values
ENUM_CORRUPTION = [
    (re.compile(r'CRITICAL = 5\s*HIGH = 4\s*MEDIUM = 3\s*LOW = 2\s*IN"{3}FO"{6} = 1'), 'CRITICAL = 5\n    HIGH = 4\n    MEDIUM = 3\n    LOW = 2\n    INFO = 1'),
]

def fix_file(path: Path):
    text = path.read_text(encoding='utf-8')
    orig = text
    # Type annotation fixes
    for pat, repl in TYPE_CORRUPTIONS:
        text = pat.sub(repl, text)
    # String literal fixes
    for pat, repl in STRING_CORRUPTIONS:
        text = pat.sub(repl, text)
    # Attribute assignment fixes
    for pat, repl in ATTR_CORRUPTION:
        text = pat.sub(repl, text)
    # Function/class call fixes
    for pat, repl in FUNC_CALL_CORRUPTION:
        text = pat.sub(repl, text)
    # Enum value fixes
    for pat, repl in ENUM_CORRUPTION:
        text = pat.sub(repl, text)
    # Remove injected quote sequences in docstrings (replace with standard triple quotes)
    text = re.sub(r'"{3,}[^\n]*?"{3,}', '"""', text)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print(f"Fixed: {path}")

if __name__ == "__main__":
    for pyfile in TARGET_DIR.glob('*.py'):
        fix_file(pyfile)
    print("Batch type and string corruption fix complete.")
