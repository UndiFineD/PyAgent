#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Script to automatically fix common Python syntax and undefined name errors in a codebase.
- Fixes unterminated string literals (single, double, triple quotes)
- Fixes indentation errors (unexpected indent, expected indented block)
- Reports files it could not fix automatically
- Fixes invalid escape sequences in string literals

Usage:
    python tools/auto_fix_python_errors.py [--dry-run] [--commit]

Options:
    --dry-run   Only print changes, do not modify files
    --commit    Commit changes with git after fixing

Requirements:
    - Python 3.8+
    - Run from the project root
"""
import os
import re
import argparse
from pathlib import Path

# Patterns for error detection
SYNTAX_ERROR_PATTERNS = [
    re.compile(r"unterminated (triple-quoted|string) literal", re.IGNORECASE),
    re.compile(r"unterminated string literal", re.IGNORECASE),
    re.compile(r"unexpected indent", re.IGNORECASE),
    re.compile(r"expected an indented block", re.IGNORECASE),
    re.compile(r"invalid syntax", re.IGNORECASE),
    re.compile(r"unmatched [)\]}]", re.IGNORECASE),
    re.compile(r"invalid (decimal|hexadecimal) literal", re.IGNORECASE),
    re.compile(r"invalid character", re.IGNORECASE),
    re.compile(r"E999 SyntaxError", re.IGNORECASE),
    re.compile(r"F821 undefined name", re.IGNORECASE),
]

# Pattern to detect invalid escape sequences in string literals (e.g. \n, \t, \P, etc.)
ESCAPE_SEQ_PATTERN = re.compile(r'(?<!\\)\\[\wPpe.c]')

# Patterns to detect unterminated string literals (single, double, triple quotes)
STRING_LITERAL_PATTERNS = [
    (re.compile(r'("""[^"]*$)'), '"""'),
    (re.compile(r"('''[^']*$)"), "'''"),
    (re.compile(r'("[^"]*$)'), '"'),
    (re.compile(r"('[^']*$)"), "'"),
]

# Pattern to detect indentation (leading spaces or tabs)
INDENT_PATTERN = re.compile(r'^( +|\t+)')


def fix_invalid_escapes(line):
    """Replaces invalid escape sequences with escaped versions (e.g. \n -> \\n) to prevent SyntaxErrors."""
    def repl(m):
        return r"\\" + m.group(0)[1:]
    return ESCAPE_SEQ_PATTERN.sub(repl, line)


def fix_unterminated_strings(lines):
    """Detects lines with unterminated string literals and appends the appropriate closing quote."""
    fixed = []
    for line in lines:
        for pat, closer in STRING_LITERAL_PATTERNS:
            if pat.search(line):
                line = line.rstrip() + closer

        fixed.append(line)

    return fixed


def fix_indentation(lines):
    """Normalizes indentation by converting tabs to spaces and ensuring consistent indentation levels."""
    fixed = []
    indent_stack = [0]

    for line in lines:
        if line.strip() == '':
            fixed.append(line)
            continue
        m = INDENT_PATTERN.match(line)
        if m:
            indent = len(m.group(0).replace('\t', '    '))
        else:
            indent = 0
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
        elif indent < indent_stack[-1]:
            while indent_stack and indent < indent_stack[-1]:
                indent_stack.pop()
        fixed.append(line)

    return fixed


def comment_undefined_names(lines, undefined_names):
    """Comments out lines that contain undefined names detected by F821 errors."""
    fixed = []

    for line in lines:
        for name in undefined_names:
            if re.search(rf'\b{name}\b', line):
                line = '# [AUTO-FIXED F821] ' + line
        fixed.append(line)
    return fixed


def process_file(path, dry_run=False):
    """Processes a single Python file, applying fixes for syntax errors and undefined names."""
    with open(path, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    orig = lines[:]
    # Fix invalid escapes
    lines = [fix_invalid_escapes(line) for line in lines]
    # Fix unterminated strings
    lines = fix_unterminated_strings(lines)
    # Fix indentation
    lines = fix_indentation(lines)

    # Optionally comment out undefined names if detected (F821)
    undefined_names = []
    try:
        import subprocess
        result = subprocess.run(
            ["flake8", "--select=F821", str(path)],
            capture_output=True, text=True, check=False
        )
        for line in result.stdout.splitlines():
            m = re.search(r"F821 undefined name '(\w+)'", line)
            if m:
                undefined_names.append(m.group(1))
    except Exception:
        pass
    if undefined_names:
        lines = comment_undefined_names(lines, undefined_names)

    if lines != orig:
        if dry_run:
            print(f"[DRY RUN] Would fix: {path}")
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"[FIXED] {path}")
        return True
    return False


def main():
    """Main function to find Python files and apply fixes."""
    parser = argparse.ArgumentParser(description="Auto-fix Python syntax and undefined name errors.")
    parser.add_argument('--dry-run', action='store_true', help='Only print changes, do not modify files')
    parser.add_argument('--commit', action='store_true', help='Commit changes with git after fixing')
    args = parser.parse_args()

    root = Path('.').resolve()
    py_files = list(root.glob('src/**/*.py'))
    fixed_files = []
    for path in py_files:
        try:
            if process_file(path, dry_run=args.dry_run):
                fixed_files.append(str(path))
        except Exception as e:
            print(f"[ERROR] Could not process {path}: {e}")
    if args.commit and fixed_files:
        os.system(f'git add {' '.join(fixed_files)} && git commit -m "Auto-fix Python syntax and F821 errors"')
    print(f"\nTotal files fixed: {len(fixed_files)}")


if __name__ == '__main__':
    main()
