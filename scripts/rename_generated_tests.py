#!/usr/bin/env python3
"""Rename all *_generated_test.py to *_test.py, overwriting existing targets.
"""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
count = 0
skipped = 0
for p in ROOT.joinpath('src').rglob('*_generated_test.py'):
    target = p.with_name(p.name.replace('_generated_test.py', '_test.py'))
    try:
        # Use replace to overwrite if exists
        os.replace(p, target)
        print(f"Renamed: {p} -> {target}")
        count += 1
    except Exception as e:
        print(f"Failed: {p}: {e}")
        skipped += 1

print(f"Done. Renamed: {count}, Failed: {skipped}")
