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

"""
move_completed.py - Move completed rows from .external/tracking.md to .external/completed.md

[Brief Summary]
Small utility that scans a markdown table in .external/tracking.md, detects rows whose status column indicates completion, appends those rows to .external/completed.md (avoiding duplicates), and rewrites tracking.md without the moved rows. Runs idempotently and stamps the completed file with an ISO UTC timestamp.

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Run from the repository root where move_completed.py lives: python move_completed.py
- Intended as a simple one-off or cron-style utility; no CLI flags currently implemented.

WHAT IT DOES:
- Reads ROOT/.external/tracking.md, collects contiguous table rows (lines starting with '|'), and treats the second table column as the status.
- Detects completed rows when the status contains any of: completed, done, finished, closed (case-insensitive).
- Appends any newly found completed rows to ROOT/.external/completed.md with a timestamp comment, ensuring the exact row string is not duplicated.
- Writes back tracking.md preserving leading header/footer lines and the remaining (kept) table rows.
- Exits with 0 on success, 2 if the tracking file does not exist.

WHAT IT SHOULD DO BETTER:
- Use atomic filesystem transactions (StateTransaction / agent_state_manager) when modifying files so partial failures cannot corrupt tracking/completed files.
- Normalize rows for deduplication (trim whitespace, normalize columns) rather than comparing raw line strings to avoid false duplicates from different spacing.
- Provide a CLI (argparse) to configure paths, completion keywords, dry-run mode, and verbosity/logging instead of hard-coded constants.
- Use the logging module rather than print() for structured logs and different log levels; add unit tests around parsing, status detection, and file updates.
- Parse markdown tables robustly (handle pipes in cells, code spans, escaped pipes) instead of naive split on '|' to avoid mis-parsing complex cells.
- Preserve table header separator row (e.g., |---|---|) and ensure output tracking.md maintains a valid table structure and trailing newline semantics.
- Create backups before overwriting files and consider concurrency protections (file locks) for multi-process safety.
- Handle different encodings and large files more efficiently (streaming) and consider making timestamp format configurable.

FILE CONTENT SUMMARY:
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

"""Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.
"""
from __future__ import annotations
from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parents[2]
TRACK = ROOT / '.external' / 'tracking.md'
COMP = ROOT / '.external' / 'completed.md'


def parse_row(line: str) -> list[str] | None:
    if not line.strip().startswith('|'):
        return None
    parts = [p.strip() for p in line.strip().split('|')[1:-1]]
    return parts


def is_completed_status(s: str) -> bool:
    if not s:
        return False
    s2 = s.lower()
    for kw in ('completed', 'done', 'finished', 'closed'):
        if kw in s2:
            return True
    return False


def main():
    if not TRACK.exists():
        print('tracking file missing:', TRACK)
        return 2
    text = TRACK.read_text(encoding='utf-8', errors='ignore').splitlines()
    header_lines = []
    rows = []
    moved = []
    started_rows = False
    for ln in text:
        if ln.strip().startswith('|'):
            started_rows = True
            rows.append(ln)
        else:
            if not started_rows:
                header_lines.append(ln)
            else:
                # footer or blank after table
                header_lines.append(ln)

    # load completed existing set
    existing = set()
    if COMP.exists():
        for ln in COMP.read_text(encoding='utf-8', errors='ignore').splitlines():
            existing.add(ln.strip())

    keep = []
    for r in rows:
        parts = parse_row(r)
        if parts is None or len(parts) < 2:
            keep.append(r)
            continue
        status = parts[1]
        if is_completed_status(status):
            if r.strip() not in existing:
                moved.append(r)
        else:
            keep.append(r)

    if moved:
        COMP.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.utcnow().isoformat() + 'Z'
        with COMP.open('a', encoding='utf-8') as f:
            f.write(f'<!-- moved on {stamp} -->\n')
            for r in moved:
                f.write(r + '\n')
        print('Moved', len(moved), 'rows to', COMP)
        # write back tracking with header_lines + keep rows
        out_lines = []
        out_lines.extend(header_lines)
        out_lines.append('')
        out_lines.extend(keep)
        TRACK.write_text('\n'.join(out_lines), encoding='utf-8')
    else:
        print('No completed rows found')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
"""
from __future__ import annotations
from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parents[2]
TRACK = ROOT / '.external' / 'tracking.md'
COMP = ROOT / '.external' / 'completed.md'


def parse_row(line: str) -> list[str] | None:
    if not line.strip().startswith('|'):
        return None
    parts = [p.strip() for p in line.strip().split('|')[1:-1]]
    return parts


def is_completed_status(s: str) -> bool:
    if not s:
        return False
    s2 = s.lower()
    for kw in ('completed', 'done', 'finished', 'closed'):
        if kw in s2:
            return True
    return False


def main():
    if not TRACK.exists():
        print('tracking file missing:', TRACK)
        return 2
    text = TRACK.read_text(encoding='utf-8', errors='ignore').splitlines()
    header_lines = []
    rows = []
    moved = []
    started_rows = False
    for ln in text:
        if ln.strip().startswith('|'):
            started_rows = True
            rows.append(ln)
        else:
            if not started_rows:
                header_lines.append(ln)
            else:
                # footer or blank after table
                header_lines.append(ln)

    # load completed existing set
    existing = set()
    if COMP.exists():
        for ln in COMP.read_text(encoding='utf-8', errors='ignore').splitlines():
            existing.add(ln.strip())

    keep = []
    for r in rows:
        parts = parse_row(r)
        if parts is None or len(parts) < 2:
            keep.append(r)
            continue
        status = parts[1]
        if is_completed_status(status):
            if r.strip() not in existing:
                moved.append(r)
        else:
            keep.append(r)

    if moved:
        COMP.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.utcnow().isoformat() + 'Z'
        with COMP.open('a', encoding='utf-8') as f:
            f.write(f'<!-- moved on {stamp} -->\n')
            for r in moved:
                f.write(r + '\n')
        print('Moved', len(moved), 'rows to', COMP)
        # write back tracking with header_lines + keep rows
        out_lines = []
        out_lines.extend(header_lines)
        out_lines.append('')
        out_lines.extend(keep)
        TRACK.write_text('\n'.join(out_lines), encoding='utf-8')
    else:
        print('No completed rows found')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
