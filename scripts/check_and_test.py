#!/usr/bin/env python3
import glob, pathlib, subprocess, sys

# repair imports
subprocess.run([sys.executable, 'scripts/fix_leading_imports.py'], check=True)

# compile check
had_error = False
for path in glob.glob('**/*.py', recursive=True):
    if '__pycache__' in path:
        continue
    try:
        compile(pathlib.Path(path).read_text(), path, 'exec')
    except IndentationError as e:
        print("IndentationError in", path, e)
        had_error = True

if had_error:
    print("Found indentation errors, aborting tests.")
    sys.exit(1)

# run pytest
res = subprocess.run([sys.executable, '-m', 'pytest', '-q', '--maxfail=1'])
if res.returncode != 0:
    sys.exit(res.returncode)
