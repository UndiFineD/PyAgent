#!/usr/bin/env python3
"""Apply unified-diff patches from .external/patches_ast to workspace files.

This script applies patches conservatively: it verifies context lines before applying
and backs up original files as `.bak` when a patch is applied.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PATCH_DIR = ROOT / '.external' / 'patches_ast'


def parse_patch(patch_text: str):
    lines = patch_text.splitlines(keepends=True)
    idx = 0
    fromfile = None
    tofile = None
    hunks = []
    # find header lines
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('--- '):
            fromfile = line[4:].strip()
        elif line.startswith('+++ '):
            tofile = line[4:].strip()
        elif line.startswith('@@ '):
            break
        idx += 1
    # parse hunks
    while idx < len(lines):
        header = lines[idx]
        if not header.startswith('@@ '):
            idx += 1
            continue
        m = re.match(r"@@ -([0-9]+)(?:,([0-9]+))? \+([0-9]+)(?:,([0-9]+))? @@", header)
        if not m:
            raise ValueError('invalid hunk header: ' + header)
        old_start = int(m.group(1))
        old_len = int(m.group(2) or '1')
        new_start = int(m.group(3))
        new_len = int(m.group(4) or '1')
        idx += 1
        hunk_lines = []
        while idx < len(lines) and not lines[idx].startswith('@@ '):
            # stop at next hunk header
            hunk_lines.append(lines[idx])
            idx += 1
        hunks.append({'old_start': old_start, 'old_len': old_len, 'new_start': new_start, 'new_len': new_len, 'lines': hunk_lines})
    return fromfile, tofile, hunks


def apply_hunks_to_source(orig_lines: list[str], hunks: list[dict]) -> tuple[bool, list[str]]:
    new_lines: list[str] = []
    cur = 0  # index in orig_lines
    for h in hunks:
        old_start = h['old_start'] - 1  # convert to 0-based
        # append unchanged before hunk
        if old_start > cur:
            new_lines.extend(orig_lines[cur:old_start])
            cur = old_start
        # process hunk
        hunk_lines = h['lines']
        for hl in hunk_lines:
            if hl.startswith(' '):
                expected = hl[1:]
                if cur >= len(orig_lines) or orig_lines[cur] != expected:
                    return False, orig_lines
                new_lines.append(expected)
                cur += 1
            elif hl.startswith('-'):
                expected = hl[1:]
                if cur >= len(orig_lines) or orig_lines[cur] != expected:
                    return False, orig_lines
                # remove: skip original line
                cur += 1
            elif hl.startswith('+'):
                new_lines.append(hl[1:])
            else:
                # unknown prefix, treat as context
                expected = hl
                if cur < len(orig_lines):
                    new_lines.append(expected)
                    cur += 1
                else:
                    new_lines.append(expected)
    # append remainder
    if cur < len(orig_lines):
        new_lines.extend(orig_lines[cur:])
    return True, new_lines


def apply_patch_file(patch_path: Path) -> bool:
    text = patch_path.read_text(encoding='utf-8')
    fromfile, tofile, hunks = parse_patch(text)
    if not tofile:
        print('Skipping patch with no target file:', patch_path)
        return False
    # strip possible a/ b/ prefixes
    if tofile.startswith('b/'):
        target = tofile[2:]
    else:
        target = tofile
    target_path = ROOT / target
    if not target_path.exists():
        print('Target does not exist for patch', patch_path, '->', target_path)
        return False
    orig_text = target_path.read_text(encoding='utf-8', errors='ignore')
    orig_lines = orig_text.splitlines(keepends=True)
    ok, new_lines = apply_hunks_to_source(orig_lines, hunks)
    if not ok:
        print('Patch context mismatch, skipping', patch_path)
        return False
    # backup original
    bak = target_path.with_suffix(target_path.suffix + '.bak')
    if not bak.exists():
        bak.write_text(orig_text, encoding='utf-8')
    target_path.write_text(''.join(new_lines), encoding='utf-8')
    print('Applied patch', patch_path, '->', target_path)
    return True


def main() -> int:
    if not PATCH_DIR.exists():
        print('No AST patches directory:', PATCH_DIR)
        return 0
    applied = 0
    for p in sorted(PATCH_DIR.glob('*.patch')):
        try:
            if apply_patch_file(p):
                applied += 1
        except Exception as e:
            print('Failed to apply patch', p, e)
    print('Applied patches:', applied)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
