#!/usr/bin/env python3
import collections
import os

root = os.getcwd()
paths = []
for dirpath, dirs, files in os.walk(root):
    # Skip any virtualenv directories (e.g. .venv, venv) in the path
    parts = dirpath.split(os.sep)
    if any(part.startswith('.venv') or part.startswith('venv') for part in parts):
        continue
    # Prevent descending into common venv folders
    dirs[:] = [d for d in dirs if not (d.startswith('.venv') or d.startswith('venv'))]
    for f in files:
        if f.endswith("_test.py"):
            paths.append(os.path.join(dirpath, f))

counts = collections.Counter(os.path.basename(p) for p in paths)
print("total_test_files:", len(paths))
print()
for name, count in counts.most_common(40):
    print(f"{count:4}  {name}")
    sample = [p for p in paths if os.path.basename(p) == name][:5]
    for s in sample:
        print("     ", s)
    print()
