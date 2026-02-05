#!/usr/bin/env python3
"""Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.
"""
from __future__ import annotations
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = ROOT / 'src' / 'external_candidates'
SRC_TOP = ROOT / 'external_candidates'

if not SRC_TOP.exists():
    print("No top-level 'external_candidates' directory found; nothing to move.")
    sys.exit(0)

moved = []
for dirpath, dirnames, filenames in os.walk(SRC_TOP):
    rel_dir = os.path.relpath(dirpath, SRC_TOP)
    if rel_dir == '.':
        rel_dir = ''
    target_dir = SRC_ROOT / rel_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    for fn in filenames:
        srcf = Path(dirpath) / fn
        dstf = target_dir / fn
        try:
            # try git mv first
            ret = subprocess.run(['git', 'mv', str(srcf), str(dstf)], cwd=ROOT, check=False)
            if ret.returncode != 0:
                # fallback
                shutil.move(str(srcf), str(dstf))
        except Exception:
            shutil.move(str(srcf), str(dstf))
        moved.append((str(srcf), str(dstf)))

# remove empty directories under SRC_TOP
for dirpath, dirnames, filenames in os.walk(SRC_TOP, topdown=False):
    try:
        os.rmdir(dirpath)
    except Exception:
        pass

print(f"Moved {len(moved)} files into {SRC_ROOT}")
for a, b in moved[:200]:
    print(a, '->', b)

if len(moved) == 0:
    print('No files moved.')
else:
    print('Done.')
