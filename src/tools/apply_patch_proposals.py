#!/usr/bin/env python3
"""Apply conservative patch proposals generated from bandit findings.

This script re-uses the heuristics in `prepare_refactor_patches.py` to
produce safe, text-based replacements for flagged lines (e.g. comment out
risky imports, replace eval/exec with a RuntimeError), writes a backup
`*.bak` and updates the target file in-place.

This is intentionally conservative and deterministic so it can run
automatically in CI or overnight runs.
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH_DIR = ROOT / '.external' / 'patches'
STATIC_DIR = ROOT / '.external' / 'static_checks'


def main() -> int:
    try:
        from src.tools import prepare_refactor_patches as prep
    except Exception:
        # fallback: try to import by path
        sys.path.insert(0, str(ROOT / 'src'))
        from tools import prepare_refactor_patches as prep

    try:
        data = prep.load_bandit()
    except FileNotFoundError:
        print('No bandit JSON found; nothing to apply')
        return 0

    agg = prep.aggregate(data)
    applied = 0
    for fn, meta in agg.items():
        p = Path(fn)
        if not p.exists():
            continue
        try:
            lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception as e:
            print('Failed reading', p, e)
            continue

        handled = set()
        modified = False
        for f in meta.get('findings', []):
            ln = f.get('line') or 0
            if ln <= 0 or ln > len(lines):
                continue
            if ln in handled:
                continue
            orig = lines[ln - 1]
            s = orig.strip()
            # Skip risky/easily-broken contexts
            if s.startswith(('def ', 'class ', 'assert', '@', 'return', 'yield', 'if ', 'for ', 'while ', 'with ', 'try:', 'except')):
                continue
            # Conservative application rules:
            # - comment out imports
            # - replace eval/exec/compile with a RuntimeError
            # - replace subprocess/os.system/Popen usages with a RuntimeError
            applied_here = False
            if s.startswith('import ') or s.startswith('from '):
                msg = f"  # PATCH_APPLIED: commented risky import ({f.get('severity')})"
                lines[ln - 1] = '# ' + orig + msg
                applied_here = True
            elif any(k in s for k in ('eval', 'exec', 'compile')):
                # Found potential dynamic execution usage — conservatively replace.
                # Use of eval() is highly insecure — intentional detection here
                lines[ln - 1] = (
                    "raise RuntimeError('Refactor required: remove dynamic execution; "
                    "see .external/patches')"
                )
                applied_here = True
            elif 'subprocess' in s or 'os.system' in s or 'Popen' in s:
                lines[ln - 1] = "raise RuntimeError('Refactor required: avoid running subprocesses directly')"
                applied_here = True

            if applied_here:
                handled.add(ln)
                modified = True

        if modified:
            bak = p.with_suffix(p.suffix + '.bak')
            try:
                if not bak.exists():
                    shutil.copy2(p, bak)
            except Exception as e:
                print('Failed to backup', p, e)
                continue
            try:
                p.write_text('\n'.join(lines), encoding='utf-8')
                applied += 1
                print('Applied proposals to', p)
            except Exception as e:
                print('Failed to write modified file', p, e)
                # attempt to restore backup
                try:
                    shutil.copy2(bak, p)
                except Exception:
                    pass

    print(f'Applied proposals to {applied} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
