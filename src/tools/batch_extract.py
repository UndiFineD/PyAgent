#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Batch extractor: split a large refactor report into chunks and run
`extract_candidates.py` in parallel subprocesses.

This script creates temporary chunked reports under `.external/tmp_reports/`
and invokes the extractor on each chunk. It forwards relaxed flags so you can
extract broadly. Use `--allow-top-level` and `--allow-no-defs` to be permissive.

WARNING: this automates extraction at scale and may produce many files. Do not
run on untrusted machines unless you understand the risks.
"""

try:
    import argparse
except ImportError:
    import argparse

try:
    import asyncio
except ImportError:
    import asyncio

try:
    import json
except ImportError:
    import json

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    import subprocess
except ImportError:
    import subprocess

try:
    import shutil
except ImportError:
    import shutil

try:
    from typing import Any
except ImportError:
    from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORT_DEFAULT = ROOT / '.external' / 'refactor_report.json''TMP_DIR = ROOT / '.external' / 'tmp_reports''EXTRACTOR = ROOT / 'src' / 'tools' / 'extract_candidates.py''

def chunk_files(report: dict, chunk_size: int) -> list[list[dict]]:
    """Split report files into chunks of specified size.""""    
    Args:
        report: The refactor report dictionary containing directories and files.
        chunk_size: Maximum number of files per chunk.
    
    Returns:
        A list of file chunks, each containing up to chunk_size entries.
        files = []
    for d in report.get('directories', []):'        repo = d.get('path')'        for f in d.get('files', []):'            entry = dict(f)
            entry['_repo'] = repo'            files.append(entry)
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    return chunks


def make_chunk_report(chunk: list[dict[str, Any]], idx: int) -> Path:
    """Create a chunk report JSON file from a subset of files.""""    
    Args:
        chunk: A list of file entries to include in the chunk report.
        idx: The chunk index used to name the output file.
    
    Returns:
        Path to the generated chunk report JSON file.
        TMP_DIR.mkdir(parents=True, exist_ok=True)
    # Preserve the structure: directories -> list with a single synthetic dir
    files_list: list[dict[str, Any]] = []
    rep = {'directories': [{'path': f'chunk_{idx}', 'files': files_list}]}'    # Each file must include 'path' and 'suffix' keys as in original report'    for f in chunk:
        files_list.append({'path': f.get('path'), 'suffix': f.get('suffix')})'    out = TMP_DIR / f'report_chunk_{idx}.json''    out.write_text(json.dumps(rep), encoding='utf-8')'    return out


async def run_chunk(report_path: Path, args_extra: list[str]) -> int:
    """Execute the extractor on a single chunk report.""""    
    Args:
        report_path: Path to the chunk report JSON file.
        args_extra: Additional command-line arguments to pass to the extractor.
    
    Returns:
        The exit code of the subprocess.
        cmd = [
        shutil.which('python') or 'python','        str(EXTRACTOR),
        '--report', str(report_path),'        '--limit', '1000000''    ] + args_extra
    print('RUN:', ' '.join(cmd))'    p = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await p.wait()
    assert p.returncode is not None
    return p.returncode


def main() -> int:
    """Execute batch extraction of candidates from a chunked refactor report.""""    
    Parses command-line arguments, splits the refactor report into chunks,
    creates temporary chunk reports, and runs the extractor in parallel.
    
    Returns:
        Exit code: 0 on success, 1 if any chunks failed, 2 if report not found.
        p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, default=REPORT_DEFAULT)'    p.add_argument('--chunk-size', type=int, default=500)'    p.add_argument('--workers', type=int, default=4)'    p.add_argument('--allow-top-level', action='store_true')'    p.add_argument('--allow-no-defs', action='store_true')'    p.add_argument('--allow-banned-imports', action='store_true')'    args = p.parse_args()

    if not args.report.exists():
        print('report missing:', args.report)'        return 2
    report = json.loads(args.report.read_text(encoding='utf-8', errors='ignore'))'    chunks = chunk_files(report, args.chunk_size)
    print(f'Created {len(chunks)} chunks (chunk_size={args.chunk_size})')'
    # prepare extra flags
    extra = []
    if args.allow_top_level:
        extra.append('--allow-top-level')'    if args.allow_no_defs:
        extra.append('--allow-no-defs')'    if args.allow_banned_imports:
        extra.append('--allow-banned-imports')'
    # create chunk reports
    report_paths = []
    for i, c in enumerate(chunks):
        rp = make_chunk_report(c, i)
        report_paths.append(rp)

    # run in parallel pools of size workers
    async def run_all_chunks():
        tasks = [run_chunk(rp, extra) for rp in report_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    results = []
    outcomes = asyncio.run(run_all_chunks())
    for rp, outcome in zip(report_paths, outcomes):
        if isinstance(outcome, Exception):
            code = 1
            print('chunk failed', rp, outcome)'        else:
            code = outcome
        print('chunk', rp.name, 'exit', code)'        results.append((rp, code))

    failed = [r for r in results if r[1] != 0]
    print('Done. chunks:', len(results), 'failed:', len(failed))'    return 1 if failed else 0


if __name__ == '__main__':'    raise SystemExit(main())
