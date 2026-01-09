import os
import re

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
