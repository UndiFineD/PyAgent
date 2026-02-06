#!/usr/bin/env python3
import os
from pathlib import Path

ROOT = Path.cwd()
SEARCH_DIRS = [ROOT / 'src', ROOT / 'tests', ROOT / 'config']
OUT = ROOT / '.tmp' / 'agent_cache_matches.txt'

def search():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8') as out:
        for d in SEARCH_DIRS:
            if not d.exists():
                continue
            for fp in d.rglob('*.py'):
                try:
                    text = fp.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
                if '.agent_cache' in text or 'agent_cache' in text:
                    for i, line in enumerate(text.splitlines(), start=1):
                        if '.agent_cache' in line or 'agent_cache' in line:
                            out.write(f"{fp.relative_to(ROOT)}:{i}:{line.strip()}\n")

if __name__ == '__main__':
    search()
    print('Done. Matches written to .tmp/agent_cache_matches.txt')
