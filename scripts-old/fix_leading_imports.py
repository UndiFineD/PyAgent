#!/usr/bin/env python3
"""Helper script to fix leading spaces/tabs before import statements in src/ files."""
# this wrapper simply forwards to the more robust fixer in strip_leading_import_spaces
# to keep both scripts in sync; the pytest shim calls this file for historical reasons.
from __future__ import annotations

import sys

# delegate to the main function of the specialized script
if __name__ == "__main__":
    # when running under pytest the working directory is the repo root, so this import
    # should succeed.  if it fails we fall back to a minimal reimplementation.
    try:
        from scripts.strip_leading_import_spaces import main

        sys.exit(main())
    except Exception:
        # fallback simple implementation (strip exactly one leading space/tab)
        import pathlib

        root = pathlib.Path(__file__).parent.parent
        COUNT = 0
        for p in root.rglob('src/**/*.py'):
            try:
                text = p.read_text(encoding='utf-8')
            except Exception:
                continue
            HAS_CHANGED = False
            lines = text.splitlines(keepends=True)
            for i, line in enumerate(lines):
                if line.startswith(' from ') or line.startswith('\tfrom '):
                    lines[i] = line[1:]
                    HAS_CHANGED = True
                elif line.startswith(' import ') or line.startswith('\timport '):
                    lines[i] = line[1:]
                    HAS_CHANGED = True
            if HAS_CHANGED:
                p.write_text(''.join(lines), encoding='utf-8')
                COUNT += 1
        print(f"Fixed leading-import lines in {COUNT} files.")
