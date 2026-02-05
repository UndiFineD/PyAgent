#!/usr/bin/env python3
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / 'src' / 'external_candidates' / 'auto'
DEST_DIR = ROOT / 'src' / 'external_candidates' / 'cleaned'

def sanitize(name: str) -> str:
    base = Path(name).stem
    s = base.lower()
    s = re.sub(r'[^0-9a-z_]', '_', s)
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    if not s:
        s = 'module'
    if s[0].isdigit():
        s = '_' + s
    return s + '.py'

def main():
    if not SRC_DIR.exists():
        print(f"Source dir not found: {SRC_DIR}")
        return
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for p in sorted(SRC_DIR.iterdir()):
        if p.is_file() and p.suffix == '.py':
            new_name = sanitize(p.name)
            dest = DEST_DIR / new_name
            if dest.exists():
                print(f"Skipping existing: {dest}")
                mapping[str(p)] = str(dest)
                continue
            text = p.read_text(encoding='utf-8')
            header = f"# Extracted from: {p.resolve()}\n"
            dest.write_text(header + text, encoding='utf-8')
            mapping[str(p.relative_to(ROOT))] = str(dest.relative_to(ROOT))
            print(f"Wrote: {dest}")
    map_file = DEST_DIR / 'refactor_map.json'
    map_file.write_text(json.dumps(mapping, indent=2), encoding='utf-8')
    print(f"Wrote mapping to {map_file}")

if __name__ == '__main__':
    main()
