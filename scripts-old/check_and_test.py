#!/usr/bin/env python3
"""Script to check for indentation errors and run pytest."""
import glob
import pathlib
import subprocess
import sys

# repair imports
subprocess.run([sys.executable, 'scripts/fix_leading_imports.py'], check=True)

# compile check
HAD_ERROR = False
for path in glob.glob('**/*.py', recursive=True):
    if '__pycache__' in path:
        continue
    try:
        compile(pathlib.Path(path).read_text(encoding='utf-8'), path, 'exec')
    except IndentationError as e:
        print("IndentationError in", path, e)
        HAD_ERROR = True

if HAD_ERROR:
    print("Found indentation errors, aborting tests.")
    sys.exit(1)

# run pytest
res = subprocess.run([sys.executable, '-m', 'pytest', '-q', '--maxfail=1'], check=False)
if res.returncode != 0:
    sys.exit(res.returncode)
