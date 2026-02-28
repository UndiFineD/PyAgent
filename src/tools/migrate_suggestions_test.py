#!/usr/bin/env python3
"""
Move old .suggestions/*.suggested.py files next to their original sources
and create corresponding .py.diff files.
Run from repository root:
  python tools/migrate_suggestions.py
"""
from pathlib import Path
import shutil
import difflib
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
SUG_DIR = ROOT / ".suggestions"

if not SUG_DIR.exists():
    print(".suggestions directory not found; nothing to migrate.")
    sys.exit(0)

moved = 0
for f in SUG_DIR.glob("*.suggested.py"):
    base = f.name[: -len(".suggested.py")]  # like module__sub__file.py

    # Decode the encoding that replaced path separators with double-underscores.
    # Encoding rule used when creating suggestions was: rel = path.relative_to(SRC_ROOT).as_posix().replace("/", "__")
    # That means an original '/__init__.py' becomes '____init__.py' in the encoded form
    # (two underscores for the separator + two leading underscores from the filename).
    # To decode safely, first map '____' -> '/__' then map remaining '__' -> '/'.
    # Decode algorithm: the encoding replaced '/' with '__'. A sequence of
    # underscores of length >= 2 may encode a separator plus leading
    # underscores in the filename (e.g. '/__init__.py' became '____init.py').
    # We scan runs of underscores: each run of length U >= 2 represents one
    # separator ('/') plus (U-2) literal underscores that belong to the
    # following filename component.

    def decode_encoded(name: str) -> str:
        # Treat the double-underscore pair '__' as the path separator.
        # When multiple underscores appear, the first two denote the
        # separator and any additional underscores immediately following
        # belong to the next component as literal leading underscores.
        components: list[str] = []
        cur: list[str] = []
        i = 0
        n = len(name)
        while i < n:
            # separator detection (non-overlapping)
            if i + 1 < n and name[i] == "_" and name[i + 1] == "_":
                # If the '__' is immediately followed by a dot or end-of-string,
                # it's unlikely to be a path separator; treat as literal underscores.
                if i + 2 >= n or name[i + 2] == ".":
                    cur.append("__")
                    i += 2
                    continue
                # finish current component
                components.append("".join(cur))
                cur = []
                i += 2
                # consume any additional underscores as leading underscores
                while i < n and name[i] == "_":
                    cur.append("_")
                    i += 1
                continue
            # normal char or single underscore literal
            cur.append(name[i])
            i += 1

        components.append("".join(cur))
        # drop a leading empty component (happens when name started with
        # an encoded separator for a leading-underscore filename)
        if components and components[0] == "":
            components = components[1:]
        return "/".join(components)

    rel = decode_encoded(base)
    src_candidate = SRC_ROOT / rel
    if not src_candidate.exists():
        print(f"WARNING: original not found for {f.name}; skipping")
        continue

    suggested_dest = src_candidate.with_name(src_candidate.stem + ".suggested" + src_candidate.suffix)
    suggested_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(f), str(suggested_dest))
    # build diff
    try:
        orig_text = src_candidate.read_text(encoding="utf-8")
    except Exception:
        orig_text = ""
    new_text = suggested_dest.read_text(encoding="utf-8")
    diff_lines = list(
        difflib.unified_diff(
            orig_text.splitlines(),
            new_text.splitlines(),
            fromfile=str(src_candidate),
            tofile=str(suggested_dest),
            lineterm="",
        )
    )
    if diff_lines:
        diff_path = src_candidate.with_suffix(src_candidate.suffix + ".diff")
        diff_path.write_text("\n".join(diff_lines) + "\n", encoding="utf-8")
    moved += 1

print(f"Migration complete. Files moved: {moved}")
