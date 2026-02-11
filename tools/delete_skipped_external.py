#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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