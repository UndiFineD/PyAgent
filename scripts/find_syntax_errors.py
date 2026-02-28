#!/usr/bin/env python3
"""Scan Python files under src/ for syntax errors and report them."""
import os
import sys
import traceback

root = os.path.join(os.path.dirname(__file__), "..")
root = os.path.abspath(root)
src = os.path.join(root, "src")

errors = []
for dirpath, _, filenames in os.walk(src):
    for fn in filenames:
        if not fn.endswith('.py'):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, 'rb') as fh:
                srcb = fh.read()
            compile(srcb, path, 'exec')
        except SyntaxError as e:
            errors.append((path, e.lineno, e.msg))
        except Exception:
            errors.append((path, None, traceback.format_exc()))

if not errors:
    print('No syntax errors found')
    sys.exit(0)

print('Syntax errors found:')
for p, ln, msg in errors:
    if ln:
        print(f"- {p}:{ln} -> {msg}")
    else:
        print(f"- {p} -> {msg}")

sys.exit(2)
