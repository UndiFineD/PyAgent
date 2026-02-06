#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path('C:/DEV/PyAgent')
OUT = ROOT / '.tmp' / 'agent_cache_matches_all.txt'
SKIP_DIRS = {'.external', '.venv', 'target', 'node_modules', '.git', 'rust_core', 'agents', 'agent_store'}

def walk_and_find():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    found = 0
    with OUT.open('w', encoding='utf-8') as out:
        for p in ROOT.rglob('*'):
            try:
                if p.is_dir():
                    if p.name in SKIP_DIRS:
                        continue
                if not p.is_file():
                    continue
                if p.suffix.lower() not in ('.py', '.json', '.toml', '.yaml', '.yml', '.ini', '.txt'):
                    continue
                text = p.read_text(encoding='utf-8', errors='ignore')
                if '.agent_cache' in text or 'agent_cache' in text:
                    for i, line in enumerate(text.splitlines(), start=1):
                        if '.agent_cache' in line or 'agent_cache' in line:
                            out.write(f"{p.relative_to(ROOT)}:{i}:{line.strip()}\n")
                            found += 1
            except Exception:
                continue
    print('Wrote', OUT, 'matches:', found)

if __name__ == '__main__':
    walk_and_find()
