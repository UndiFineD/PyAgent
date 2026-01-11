#!/usr/bin/env python3
"""
Debug script to check for consistency in _record calls across the workspace.
"""
import os
import re

def main() -> None:
    root = "src"
    findings = []

    for r, d, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(r, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        if "self._record(" in content and "def _record(" not in content:
                            findings.append(path)
                except Exception:
                    pass

    print("\n".join(findings))

if __name__ == "__main__":
    main()
