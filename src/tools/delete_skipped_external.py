#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

repo = Path.cwd()
mapf = repo / 'src' / 'external_candidates' / 'ingested' / 'batch_refactor_map.json'
out_log = repo / 'scripts' / 'delete_skipped_external.log'

if not mapf.exists():
    print('Mapping file not found:', mapf)
    raise SystemExit(1)

with mapf.open('r', encoding='utf-8') as f:
    data = json.load(f)

deleted = []
errors = []
missing = []
for key in data.keys():
    p = repo / '.external' / key
    try:
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            deleted.append(str(p))
        else:
            missing.append(str(p))
    except Exception as e:
        errors.append(f"{p}: {e}")

with out_log.open('w', encoding='utf-8') as f:
    f.write(f"deleted_count:{len(deleted)}\n")
    for d in deleted:
        f.write(f"DEL:{d}\n")
    f.write(f"missing_count:{len(missing)}\n")
    for m in missing:
        f.write(f"MISS:{m}\n")
    f.write(f"errors_count:{len(errors)}\n")
    for e in errors:
        f.write(f"ERR:{e}\n")

print(f"Done. deleted={len(deleted)} missing={len(missing)} errors={len(errors)}")