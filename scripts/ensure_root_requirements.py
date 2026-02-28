#!/usr/bin/env python3
"""Ensure root requirements.txt includes all package lines from requirements/*.txt.
Generates a flattened list appended to requirements.txt under an auto-generated header.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
req_dir = root / 'requirements'
root_req = root / 'requirements.txt'

files = []
for p in sorted(req_dir.glob('*.txt')):
    files.append(p)

packages = set()
for f in files:
    for ln in f.read_text(encoding='utf-8').splitlines():
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('-r'):
            # referenced file; skip (we already include all files in directory)
            continue
        packages.add(s)

# Preserve existing header if present
header_lines = [
    '# PyAgent Requirements (Federated)',
    '# Optimized for Python 3.12',
    '# Main entry point - includes all sub-requirements',
    '',
    '-r requirements/base.txt',
    '-r requirements/dev.txt',
    '-r requirements/ml.txt',
    '',
]

flat_lines = ['# --- Flattened requirements (auto-generated) ---', '']
for pkg in sorted(packages):
    flat_lines.append(pkg)

content = '\n'.join(header_lines + flat_lines) + '\n'

# Backup existing requirements.txt if present
if root_req.exists():
    bk = root_req.with_suffix('.txt.bak')
    root_req.replace(bk)
    print(f'Backed up existing requirements.txt -> {bk}')

root_req.write_text(content, encoding='utf-8')
print(f'Wrote {root_req} with {len(packages)} unique package entries')
