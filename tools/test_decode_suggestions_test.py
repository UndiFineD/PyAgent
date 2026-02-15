#!/usr/bin/env python3
"""Small script to test decoding of encoded suggestion filenames.

Usage:
  python tools/test_decode_suggestions.py
"""
from typing import List


def decode_encoded(name: str) -> str:
    """Decode the filename encoding used by migrate_suggestions.

    Runs of underscores are interpreted as: a run of length U>=2 encodes one
    directory separator ('/') plus (U-2) literal leading underscores in the
    following component. Single underscores are literal.
    """
    components: List[str] = []
    cur: List[str] = []
    i = 0
    n = len(name)
    while i < n:
        if i + 1 < n and name[i] == "_" and name[i + 1] == "_":
            # If '__' is immediately followed by a dot or end-of-string,
            # it's more likely literal underscores than a separator.
            if i + 2 >= n or name[i + 2] == ".":
                cur.append("__")
                i += 2
                continue
            components.append("".join(cur))
            cur = []
            i += 2
            while i < n and name[i] == "_":
                cur.append("_")
                i += 1
            continue
        cur.append(name[i])
        i += 1

    components.append("".join(cur))
    if components and components[0] == "":
        components = components[1:]
    return "/".join(components)


def main() -> None:
    examples = [
        "logic__agents__cognitive__context__engines__knowledge_mixins____init__.py",
        "src__module__submodule__file.py.suggested.py",
        "core____init__.py",
        "a__b____c__d______e.py",
    ]

    for e in examples:
        print("encoded:", e)
        print("decoded:", decode_encoded(e))
        print()


if __name__ == "__main__":
    main()
