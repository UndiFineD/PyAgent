#!/usr/bin/env python3
# Fix malformed generated test filenames in src/
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Fix generated test filename collisions')
parser.add_argument('--root', default='src', help='Root directory to scan')
parser.add_argument('--force', action='store_true', help='Overwrite existing targets')
parser.add_argument('--remove', action='store_true', help='Remove malformed source files when target exists')
args = parser.parse_args()

root = Path(args.root)
renames = []
for p in root.rglob('*.py'):
    name = p.name
    # patterns to fix:
    # 1) something.py_test.py -> something_test.py
    if name.endswith('.py_test.py'):
        target = p.with_name(name.replace('.py_test.py', '_test.py'))
        renames.append((p, target))
        continue
    # 2) something_test_test.py -> something_test.py
    if name.endswith('_test_test.py'):
        target = p.with_name(name.replace('_test_test.py', '_test.py'))
        renames.append((p, target))
        continue

moved = 0
skipped = 0
conflicts = 0
for src, dst in renames:
    if dst.exists():
        if args.force:
            os.replace(src, dst)
            moved += 1
            print(f"Overwrote: {src} -> {dst}")
        elif args.remove:
            os.remove(src)
            moved += 1
            print(f"Removed duplicate source: {src} (target exists: {dst})")
        else:
            print(f"Skip (target exists): {src} -> {dst}")
            skipped += 1
            conflicts += 1
    else:
        os.replace(src, dst)
        print(f"Renamed: {src} -> {dst}")
        moved += 1

print(f"Summary: renamed={moved}, skipped={skipped}, conflicts={conflicts}")
