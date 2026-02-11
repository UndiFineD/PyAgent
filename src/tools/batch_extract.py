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

"""Batch extractor: split a large refactor report into chunks and run
`extract_candidates.py` in parallel subprocesses.

This script creates temporary chunked reports under `.external/tmp_reports/`
and invokes the extractor on each chunk. It forwards relaxed flags so you can
extract broadly. Use `--allow-top-level` and `--allow-no-defs` to be permissive.

WARNING: this automates extraction at scale and may produce many files. Do not
run on untrusted machines unless you understand the risks.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import shutil
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORT_DEFAULT = ROOT / '.external' / 'refactor_report.json'
TMP_DIR = ROOT / '.external' / 'tmp_reports'
EXTRACTOR = ROOT / 'src' / 'tools' / 'extract_candidates.py'


def chunk_files(report: dict, chunk_size: int) -> list[list[dict]]:
    files = []
    for d in report.get('directories', []):
        repo = d.get('path')
        for f in d.get('files', []):
            entry = dict(f)
            entry['_repo'] = repo
            files.append(entry)
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    return chunks


def make_chunk_report(chunk: list[dict[str, Any]], idx: int) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    # Preserve the structure: directories -> list with a single synthetic dir
    files_list: list[dict[str, Any]] = []
    rep = {'directories': [{'path': f'chunk_{idx}', 'files': files_list}]}
    # Each file must include 'path' and 'suffix' keys as in original report
    for f in chunk:
        files_list.append({'path': f.get('path'), 'suffix': f.get('suffix')})
    out = TMP_DIR / f'report_chunk_{idx}.json'
    out.write_text(json.dumps(rep), encoding='utf-8')
    return out


def run_chunk(report_path: Path, args_extra: list[str]) -> int:
    cmd = [
        shutil.which('python') or 'python',
        str(EXTRACTOR),
        '--report', str(report_path),
        '--limit', '1000000'
    ] + args_extra
    print('RUN:', ' '.join(cmd))
    p = subprocess.run(cmd)
    return p.returncode


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, default=REPORT_DEFAULT)
    p.add_argument('--chunk-size', type=int, default=500)
    p.add_argument('--workers', type=int, default=4)
    p.add_argument('--allow-top-level', action='store_true')
    p.add_argument('--allow-no-defs', action='store_true')
    p.add_argument('--allow-banned-imports', action='store_true')
    args = p.parse_args()

    if not args.report.exists():
        print('report missing:', args.report)
        return 2
    report = json.loads(args.report.read_text(encoding='utf-8', errors='ignore'))
    chunks = chunk_files(report, args.chunk_size)
    print(f'Created {len(chunks)} chunks (chunk_size={args.chunk_size})')

    # prepare extra flags
    extra = []
    if args.allow_top_level:
        extra.append('--allow-top-level')
    if args.allow_no_defs:
        extra.append('--allow-no-defs')
    if args.allow_banned_imports:
        extra.append('--allow-banned-imports')

    # create chunk reports
    report_paths = []
    for i, c in enumerate(chunks):
        rp = make_chunk_report(c, i)
        report_paths.append(rp)

    # run in parallel pools of size workers
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_chunk, rp, extra): rp for rp in report_paths}
        for fut in as_completed(futs):
            rp = futs[fut]
            try:
                code = fut.result()
            except Exception as e:
                code = 1
                print('chunk failed', rp, e)
            print('chunk', rp.name, 'exit', code)
            results.append((rp, code))

    failed = [r for r in results if r[1] != 0]
    print('Done. chunks:', len(results), 'failed:', len(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
